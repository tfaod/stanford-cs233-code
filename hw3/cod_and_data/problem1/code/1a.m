
% 1a

% load all image

# in same directory as 100chairs_rendering
H=cell(100)

PATH="cs233"
for i=1:100
    Hj=zeros(16,36,225)
    for j=1:16
    	chair=sprintf(PATH+"/100chairs_rendering/%03d_%d.png",i,j)
    	I=im2single(imread(chair))
    	% resize image
    	J=imresize(I,[120,120])
    	% run hog() on image
    	% output of hog is (15,15,36)
    	H_I=hog(I)
    	Hj(j,:,:)=size(reshape(permute(H_I,[3,1,2]),size(H_I,3),[]))	
    end
    H(i)=Hj
end

% Also submit a visualization of the computed HoG features for the shapes:
view

% concatenate into (VxH) dim vector 


