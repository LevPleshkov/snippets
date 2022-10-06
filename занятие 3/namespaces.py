# buil-it
dir(__builtins__)

# global
country = 'United Kingdom'
print(f'global: {country}')
# print(globals())

def another_country():
    # enclosing
    # global country
    country = 'New Zealand'
    print(f'enclosing: {country}')

    def one_more_country():
        # local
        nonlocal country
        country = 'Lesoto'
        print(f'local: {country}')
        # print(locals())

    one_more_country()
    print(f'enclosing: {country}')

another_country()

print(f'global: {country}')
