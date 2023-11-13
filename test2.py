def trip_cost_calculation(**kwargs):
    distance = kwargs.get('distance')
    base_fare = kwargs.get('base_fare')
    price_per_km = kwargs.get('price_per_km')
    if distance <= 3:
        return base_fare
    else:
        return base_fare + (distance - 3) * price_per_km


trip_cost = trip_cost_calculation(distance=20.5, base_fare=100, price_per_km=12)
print(f'Стоимость поездки: {trip_cost}')

