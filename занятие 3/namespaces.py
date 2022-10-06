# buil-it — пространство встроенных имен
# (запускается из интерактивной консоли python)
dir(__builtins__)

# global - глобальное пространство имен,
# совпадает с модулем
country = 'United Kingdom'
print(f'global: {country}')
# print(globals())

# в функции создается локальное пространство имен,
# которое может вмещать (enclose) другие локальные
def another_country():
    # enclosing
    # global country
    country = 'New Zealand'
    print(f'enclosing: {country}')

    # пространство этой функции будет "самым" локальным
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
