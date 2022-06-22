import uuid
import pdal


class Tile:
    def __init__(self, filename, args=None):
        self.filename = filename
        self.args = args

    def pipeline(self):
        name = uuid.uuid4()
        output_dir = self.args['output_dir']
        output_filename = f'{output_dir}/{name}.las'
        reader = pdal.Reader(
            filename=self.filename
        )
        hag_nn = pdal.Filter.hag_nn(count='100')
        range = pdal.Filter.range(limits="HeightAboveGround[:3]")
        writer = pdal.Writer.las(
            filename=output_filename
        )
        p = reader | hag_nn | range | writer
        return p

    def __str__(self):
        return f'{self.filename}'