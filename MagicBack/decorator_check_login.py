""" Created by jieyi on 5/1/17. """


class DecoratorCheckLogin:
    def __call__(self, func):
        def wrapper(*args):
            if args[0].connection is None:
                print('You\'re not login now...')
                return

            return func(*args)

        return wrapper


def main():
    print("Hello Python!")


if __name__ == '__main__':
    main()
