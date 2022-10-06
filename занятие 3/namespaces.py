# built-in
dir(__builtins__)

# global
country = 'United Kingdom'
print(f'global: {country}')
# print(globals())

def another_country():
    # enclosing
    country = 'New Zealand'
    print(f'enclosing: {country}')

    def one_more_country():
        # local
        global country
        country = 'Lesoto'
        print(f'local: {country}')

    one_more_country()
    print(f'enclosing: {country}')

if __name__ == '__main__':
    another_country()
