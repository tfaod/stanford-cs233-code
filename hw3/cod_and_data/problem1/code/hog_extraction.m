% 1a

% add path to toolbox 
% TODO - Change this to local path to Piotr’s toolbox 
% Installation: download from link below, unzip
% https://pdollar.github.io/toolbox/

% addpath(TOOLBOX_PATH+"toolbox");
% addpath(TOOLBOX_PATH+"toolbox/channels");

function H=hog_extraction()

H={};
H{100}=0;
% TODO - Change this to local path to image file
IMG_PATH="";
for i=1:100
	Hj=zeros(16,36*225,1);
	for j=1:16
		chair=sprintf(IMG_PATH+"100chairs_rendering/%03d_%d.png",i,j-1);
                I=im2single(imread(chair));
		% resize image
		J=imresize(I,[120,120]);
		% run hog() on image
		% output of hog is (15,15,36)
		H_J=hog(J);
		Hj(j,:)=H_J(:);
	end
	% concatenate into (VxH) dim vector 
	H{i}=squeeze(Hj);
end
end

