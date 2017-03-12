
class Func(object):
    def __init__(self, f, *args, **kwargs):
        self.function = f
        self.args = args
        self._kwargs = kwargs

    @property
    def kwargs(self):
        return self._kwargs

    @kwargs.setter
    def kwargs(self, new_kwargs):
        if type(new_kwargs) != dict:
            raise TypeError('new_kwargs is not a dict')

        for key in new_kwargs:
            self._kwargs[key] = new_kwargs[key]

    def __call__(self, frame):
        if self.kwargs:
            return self.function(frame, *self.args, **self.kwargs)
        elif self.args:
            return self.function(frame, *self.args)
        else:
            return self.function(frame)
