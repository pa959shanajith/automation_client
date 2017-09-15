#pytest script for imageverification unit testing

def func(file1,file2):
    from PIL import Image
    import numpy as np

    img1 = Image.open(file1)
    img2 = Image.open(file2)
    width1, height1 = img1.size
    width2, height2 = img2.size
    size=(min(width1,width2,1024),min(height1,height2,800))
    if not(file1.split('.')[-1]=='jpg'):
        img1 = img1.convert('RGB')
        #print 'converted img 1'
    if not(file2.split('.')[-1]=='jpg'):
        img2 = img2.convert('RGB')
        #print 'converted img 2'
    img1 = img1.resize(size)
    img2 = img2.resize(size)
    imageA = np.asarray(img1)
    imageB = np.asarray(img2)
    err = np.sum((imageA.astype("float") - imageB.astype("float"))**2)

    err /= float(size[0]*size[1]*3*255*255);
    print 'err %: ',err*100,'%'
    if(err<0.0005):  # err<0.05%
        #info_msg=ERROR_CODE_DICT['MSG_IMAGE_COMPARE_PASS']
        #log.info(info_msg)
        #logger.print_on_console(info_msg)
        #methodoutput=TEST_RESULT_TRUE
        #status=TEST_RESULT_PASS
							status='true'
    else:
							status='false'
        #err_msg=ERROR_CODE_DICT['ERR_IMAGE_COMPARE_FAIL']
    return status

path='D:\\Himanshu\\imgs\\'

class TestClass(object):
    def test_same(self):
        file1=path+'testimg.jpg'
        file2=path+'testimg.jpg'
        assert func(file1,file2) == 'true'
    def test_jpg_png(self):
        x = "this"
        file1=path+'testimg.jpg'
        file2=path+'testimg.png'
        assert func(file1,file2) == 'true'
    def test_jpg_gif(self):
        file1=path+'testimg.jpg'
        file2=path+'testimg.gif'
        assert func(file1,file2) == 'true'
    def test_lines(self):
        file1=path+'testimg.jpg'
        file2=path+'testimg_lines.jpg'
        assert func(file1,file2) == 'false'
    def test_lines_png(self):
        file1=path+'testimg.jpg'
        file2=path+'testimg_lines.png'
        assert func(file1,file2) == 'false'
    def test_diff(self):
        file1=path+'testimg.jpg'
        file2=path+'testimg_diff.jpg'
        assert func(file1,file2) == 'false'
    def tes_resize(self):
        file1=path+'testimg.jpg'
        file2=path+'testimg_resize.jpg'
        assert func(file1,file2) == 'true'
    def test_resolution(self):
        file1=path+'testimg.jpg'
        file2=path+'testimg_resolution.jpg'
        assert func(file1,file2) == 'true'
    def test_diff_gif(self):
        file1=path+'testimg.jpg'
        file2=path+'loader.gif'
        assert func(file1,file2) == 'false'
