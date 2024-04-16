from rest_framework import serializers

from .models import (
    MoviePurchases,
    OrderItems
    )


class MovieItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        fields = ['movie', 'movie_num']


class MoviePurchaseSerializer(serializers.ModelSerializer):
    items = MovieItemsSerializer(many=True)
    print(items)
    class Meta:
        model = MoviePurchases
        fields = ['order_id', 'created_at', 'total_sum', 'items']

    def create(self, validated_data, *args, **kwargs):
        items = validated_data.pop('items')
        validated_data['user'] = self.context['request'].user
        order = super().create(validated_data)
        total_sum = 0
        orders_items = []

        for item in items:
            tickets = (OrderItems(
                order=order,
                movie=item['movie'],
                movie_num=item['movie_num']
            ))
            orders_items.append(tickets)

            if item['movie'].movie_count >=item['movie_num']:
                item['movie'].movie_count -= item['movie_num']

                total_sum += item['movie'].price_som * item['movie_num']
                OrderItems.objects.bulk_create(orders_items, *args, **kwargs)
                order.total_sum = total_sum

                item['movie'].save()
                order.save()

                return order
            else:
                raise serializers.ValidationError('We do not have this movie')
            

class PurchaseHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MoviePurchases
        fields = ('order_id', 'total_sum', 'status', 'created_at', 'movie')