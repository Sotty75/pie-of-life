# dictionary

food = {'pera':'frutto','mela':'frutto', 'banana':'frutto', 'maiale':'carne', 'vitello':'carne'}


# stampa alimenti
print("Stampa alimenti:")
print()
for alimento, cat in food.items():
    print(food[alimento])

for alimento,categoria in food.copy().items():
    if categoria == 'frutto':
        del food[alimento]
        
# stampa alimenti senza frutta
print()
print("Stampa alimenti senza frutta: ")
print()
for alimento, cat in food.items():
    print(food[alimento])
