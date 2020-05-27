
% 1a

% load all image

% add path to toolbox 
% TODO - Change this to local path to Piotr’s toolbox 
% Installation: download from link below, unzip
% https://pdollar.github.io/toolbox/
TOOLBOX_PATH=""
addpath(TOOLBOX_PATH+"toolbox");
addpath(TOOLBOX_PATH+"toolbox/channels");

# in same directory as 100chairs_rendering
H=cell(100)

% TODO - Change this to local path to image file
IMG_PATH=""
for i=32:100
	Hj=zeros(16,36*225,1);
	for j=1:16
		chair=sprintf(PATH+"100chairs_rendering/%03d_%d.png",i,j-1)
		I=im2single(imread(chair));
		% resize image
		J=imresize(I,[120,120]);
		% run hog() on image
		% output of hog is (15,15,36)
		H_J=hog(J);
		Hj(j,:)=H_J(:);
		% if (i == 1)||(i==2)||(i==3):
		% 	imgname=sprintf("1a-views/%03d_%d-view.png",i,j-1);
		% 	imwrite(hogDraw(H_J),imgname,"png");
	end
	H{i}=squeeze(Hj);
end

% Also submit a visualization of the computed HoG features for the shapes: 
% i = 0 
% visualizations 1-16
% imwrite(hogDraw(H(0)))



% concatenate into (VxH) dim vector 


