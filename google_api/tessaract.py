#
# import pytesseract
# from PIL import Image
#
# def read_screen():
#
#     with io.open(path, 'rb') as image_file:
#         content = image_file.read()
#
#     # load the image as a PIL/Pillow image, apply OCR, and then delete the temporary file
#     text = pytesseract.image_to_string(Image.open(filename))
#
#
#     # show the output images
#
#     '''cv2.imshow("Image", image)
#     cv2.imshow("Output", gray)
#     os.remove(screenshot_file)
#     if cv2.waitKey(0):
#         cv2.destroyAllWindows()
#     print(text)
#     '''
#     return text
#
# # get questions and options from OCR text
# def parse_question():
#     text = read_screen()
#     lines = text.splitlines()
#     question = ""
#     options = list()
#     flag=False
#
#     for line in lines :
#         if not flag :
#             question=question+" "+line
#
#         if '?' in line :
#             flag=True
#             continue
#
#         if flag :
#             if line != '' :
#                 options.append(line)
#
#     return question, options
