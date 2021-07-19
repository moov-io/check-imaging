from io import BytesIO
import os.path

from wand.color import Color
from wand.compat import nested
from wand.drawing import Drawing
from wand.image import Image


def format_check_image_for_x9(in_file, threshold=0.5,
        out_format='tiff'):
    """ Convert an image to a black and white TIFF suitable for
    inclusion in an X9 file.

    Args:
        in_file (file): File-like object with image to convert
        threshold (float): Color value threshold for converting to black
            or white. 0.0 results in an all white image, 1.0 results in
            an all black image. First, the image will be converted to
            grayscale, then this threshold will be applied to the
            resulting color values.
        out_format (str): `tiff` (default) or `png`. Since most web
            browsers will not render TIFFs, the `png` option is useful
            for returning a preview of what the TIFF will look like.

    Returns:
        BytesIO
    """
    with Image(file=in_file, resolution=240) as img:
        # Drop meta data
        img.strip()

        # Must set resolution explicitly
        img.resolution = (240.0, 240.0)

        # Required minimum dimensions varies based on aux on-us field.
        # For brevity, using largest required minimum:
        # 8.5 inches wide at 240 DPI
        img.resize(
            width=2040,
            height=round(2040 / img.width * img.height)
        )

        # Convert to black and white
        img.transform_colorspace('gray')
        img.threshold(threshold=threshold, channel='gray')

        # File format
        if out_format == 'png':
            # TIFF with Group 4 compression is a lossless format, so PNG
            # should be a comparable preview
            img = img.convert('png')
        else:
            img.compression = 'group4'
            img = img.convert('tiff')

        # Result
        buf = BytesIO()
        img.save(file=buf)
        return buf

def convert_to_png(in_file):
    """ Convert an image to PNG format. Useful for previewing a TIFF in
    a web browser.

    Args:
        in_file (file): File-like object with image to convert

    Returns:
        BytesIO
    """
    with Image(file=in_file) as img:
        buf = BytesIO()
        img = img.convert('png')
        img.save(file=buf)
        return buf

def create_deposit_ticket_front(bank_name, issued_date, payee_name,
        item_count, amount, check_number, routing_number,
        account_number, transaction_code=''):
    """ Create the front image of a deposit ticket to include with image
    cash letter.

    Args:
        bank_name (str)
        date (date)
        payee_name (str)
        item_count (int): Number of checks included with this deposit
        amount (float): Total deposit amount
        check_number (int)
        routing_number (str)
        acount_number (str)
        transaction_code (str)

    Returns:
        BytesIO
    """
    with nested(
        Image(width=600, height=230, background=Color('white')),
        Drawing()
    ) as (img, draw):
        img.resolution = (240.0, 240.0)

        cols = [25, 400]
        rows = [26, 62, 102, 142, 202]

        # Deposit ticket text
        draw.font = 'DejaVu-Sans-Bold' # FIXME
        draw.font_size = 16
        img.annotate(bank_name, draw, left=cols[0], baseline=rows[0])
        img.annotate('CHECKING DEPOSIT', draw, left=cols[1],
                baseline=rows[0])
        draw.font_size = 12
        img.annotate('DATE: {:%Y%m%d}'.format(issued_date), draw,
                left=cols[0], baseline=rows[1])
        img.annotate('NAME: {}'.format(payee_name), draw, left=cols[0],
                baseline=rows[2])
        img.annotate('ITEMS: {}'.format(item_count), draw, left=cols[0],
                baseline=rows[3])
        img.annotate('NET DEPOSIT: ${:,.2F}'.format(amount), draw,
                left=cols[1], baseline=rows[3])

        # MICR data
        draw.font = 'MICR' # FIXME Either distribute a MICR font or use
                           # TTFQuery to locate font
        draw.font_size = 12
        micr_str = (
            '${check_number}$\t"{routing_number}"\t'
            '{account_number}$\t{transaction_code}\t%{amount:010d}%'
        ).format(
            check_number=check_number,
            routing_number=routing_number,
            account_number=account_number,
            transaction_code=transaction_code,
            amount=int(amount * 100)
        )
        img.annotate(micr_str, draw, left=cols[0], baseline=rows[4])

        # Convert image
        img.transform_colorspace('gray')
        img.threshold(threshold=.5, channel='gray')
        img.compression = 'group4'
        img = img.convert('tiff')

        # Result
        buf = BytesIO()
        img.save(file=buf)
        return buf

def create_deposit_ticket_back():
    """ Create the back side of a deposit ticket (blank image) for use
    in image cash letter.

    Returns:
        BytesIO
    """
    with Image(width=600, height=230, background=Color('white')) as img:
        img.resolution = (240.0, 240.0)
        img.compression = 'group4'
        img = img.convert('tiff')
        buf = BytesIO()
        img.save(file=buf)
        return buf

