from faker.generator import Generator


class MGenerator(Generator):

    def add_provider(self, provider, *args, **kwargs):
        """
        使add_provider支持传参给provider对象
        """
        if isinstance(provider, type):
            provider = provider(self, *args, **kwargs)

        self.providers.insert(0, provider)

        for method_name in dir(provider):
            # skip 'private' method
            if method_name.startswith('_'):
                continue

            faker_function = getattr(provider, method_name)

            if callable(faker_function):
                # add all faker method to generator
                self.set_formatter(method_name, faker_function)
