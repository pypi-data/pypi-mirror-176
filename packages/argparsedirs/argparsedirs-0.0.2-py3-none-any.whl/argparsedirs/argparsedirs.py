import os


class ReadableDir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not os.path.isdir(values):
            raise argparse.ArgumentTypeError(f"ReadableDir: {values} is not a valid path")
        if os.access(values, os.R_OK):
            setattr(namespace, self.dest, values)
        else:
            raise argparse.ArgumentTypeError(f"ReadableDir: {values} is not a readable directory")


class WriteableDir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not os.path.isdir(values):
            raise argparse.ArgumentTypeError(f"WriteableDir: {values} is not a valid path".)
        if os.access(values, os.W_OK):
            setattr(namespace, self.dest, values)
        else:
            raise argparse.ArgumentTypeError(f"WriteableDir: {values} is not a writeable directory")
