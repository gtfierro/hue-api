"""
color.py converts between HSB (HSV) 3-tuples (the format understood by the Hue
lights) and RGB 3-tuples (the format understood by most everyone else)

Author: Gabe Fierro
"""

def convert_hsb_to_canonical(hue, saturation, brightness):
    """
    Takes in a HSB 3-tuple and converts it to the canonical space
    0 <= hue <= 360
    0 <= saturation <= 1
    0 <= brightness <= 1

    Assumes the Hue Light space:
    0 <= hue <= 65535
    0 <= saturation <= 254
    0 <= brightness <= 254
    """
    hue = min(360, hue / 182.0) if hue > 360 else hue
    saturation = saturation / 254.0 if saturation > 1 else saturation
    brightness = brightness / 254.0 if brightness > 1 else brightness
    return (hue, saturation, brightness)

def convert_hsb_to_hue(hue, saturation, brightness):
    """
    Takes in HSB 3-tuple and converts it to the Hue Light space
    """
    hue = min(65535, hue * 182.0)
    saturation = saturation * 254.0
    brightness = brightness * 254.0
    return (hue, saturation, brightness)

def hsb_to_rgb(hue,saturation,brightness):
    """ 
    Takes in a 3-tuple of [hue], [saturation] and [brightness] (all float
    values) and returns a 3-tuple of (r,g,b) (all float values).
    """

    # convert from HueLight space to canonical HSV space
    hue, saturation, brightness = convert_hsb_to_canonical(hue, saturation, brightness)


    # compute chroma from hsb
    chroma = saturation * brightness
    canonicalhue = hue / 60.0
    x = chroma * (1 - abs((canonicalhue % 2) -1))

    # non-value-matched rgb values
    r1 = chroma if (canonicalhue % 5) < 1 else \
         x if (canonicalhue % 3) >= 1 and (canonicalhue % 3) < 2 else \
         0

    g1 = 0 if canonicalhue >= 4 else \
         chroma if canonicalhue >= 1 and canonicalhue < 3 else \
         x
         
    b1 = 0 if canonicalhue < 2 else \
         chroma if canonicalhue >= 3 and canonicalhue < 5 else \
         x
    
    modifier = brightness - chroma

    # add the modifier to each component
    adjusted_rgb = map(lambda x: x + modifier, (r1,g1,b1))

    # scale RGB values by 254

    return map(lambda x: x * 254.0, adjusted_rgb)




