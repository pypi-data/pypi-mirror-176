from PIL import Image

class GifMaker():
    def Make(output_filename:str, image_urls:list[str], fps:int, loop:int):
        # fps frame per second
        duration = 1/(fps / 1000)
        pil_images = []
        for image_url in image_urls:
            temp_im = Image.open(image_url)
            pil_images.append(temp_im)

        pil_images[0].save(output_filename, save_all=True, append_images=pil_images[1:], duration=duration, loop=loop)

    def PIL(output_filename:str, pil_images:list[Image.Image], fps:int, loop:int):
        # fps frame per second
        duration = 1/(fps / 1000)

        pil_images[0].save(output_filename, save_all=True, append_images=pil_images[1:], duration=duration, loop=loop)


if __name__ == '__main__':
    gifmaker = GifMaker()

    images = [
        "./test/orbital_l0_m0.png",
        "./test/orbital_l1_m0.png",        
        "./test/orbital_l1_m1.png",
        "./test/orbital_l2_m0.png",
        "./test/orbital_l2_m1.png",
        "./test/orbital_l2_m2.png",
    ]

    GifMaker.Make("output.gif", images, 1, 0)

    pil_images = []
    for image in images:
        pil_images.append(Image.open(image))

    GifMaker.PIL("output.gif", pil_images, 2, 0)
