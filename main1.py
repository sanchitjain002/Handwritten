import os
import cv2
from WordSegmentation import wordSegmentation, prepareImg


def main():
	"""reads images from data/ and outputs the word-segmentation to out/"""   
	# read input images from 'in' directory
path = os.getcwd()
imgFiles = os.listdir(path + '/out/')
direc = 'segmented words'
os.mkdir(os.path.join(path, direc))

total_segments = open(path + '/out/total_line_segments.txt','r')
file = total_segments.read()
file = int(file)
total = 0
    
for z in range(1,file+1):
    total+=1
    count = 0
    os.mkdir(os.path.join(path + '/segmented words/', str(z)))
    imgFiles = os.listdir(path + '/out/' + '%d/' % z)
    
    for (i,f) in enumerate(imgFiles):
        count+=1
        print('Segmenting words of sample %s'%f)
		
		# read image, prepare it by resizing it to fixed height and converting it to grayscale
        img = prepareImg(cv2.imread(path + '/out/' + '%d/' % z +'%s'%f), 50)
		
		# execute segmentation with given parameters
		# -kernelSize: size of filter kernel (odd integer)
		# -sigma: standard deviation of Gaussian function used for filter kernel
		# -theta: approximated width/height ratio of words, filter function is distorted by this factor
		# - minArea: ignore word candidates smaller than specified area
        res = wordSegmentation(img, kernelSize=25, sigma=11, theta=7, minArea=100)
		
		# write output to 'out/inputFileName' directory
        if not os.path.exists(path + '/segmented words/' + str(z) + '/%s'%f):
            os.mkdir(path + '/segmented words/' + str(z) + '/%s'%f)
		
		# iterate over all segmented words
        print('Segmented into %d words'%len(res))
        for (j, w) in enumerate(res):
	        (wordBox, wordImg) = w
	        (x, y, w, h) = wordBox
	        cv2.imwrite(path + '/segmented words/' + str(z)+ '/%s/%d.png'%(f, j), wordImg) # save word
	        cv2.rectangle(img,(x,y),(x+w,y+h),0,1) # draw bounding box in summary image
		    
		# output summary image with bounding boxes around words
		#cv2.imwrite('../out/%s/summary.png'%f, img)
    file = open(path + '/segmented words/' + str(z) + '/segments.txt','w')
    file.write("%d" % count)
    file.close()   

        
file = open(path + '/segmented words/total_segments.txt','w')
file.write("%d" % total)
file.close()

if __name__ == '__main__':
	main()