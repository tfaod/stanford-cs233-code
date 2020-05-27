% 1b

% TOOLBOX_PATH=""
% addpath(TOOLBOX_PATH+"toolbox");
% addpath(TOOLBOX_PATH+"toolbox/channels");

function D=pairwise_dissimilarity()

H=hog_extraction()
% each C(i,j,z) is L2 difference of img i, j with angle difference z*pi/8 at 
C=zeros(100,100,16);

for i=1:100
	% shape is (16,-)
	Si=H{i}(1);
        for j=1:100
		for theta=1:16
			Sj=H{j}(theta);
			C(i,j,theta)=norm(Sj-Si);
		end
	end
end


% populate D
% D(i,j,z1,z2)  corresponds to difference at angles with index z1, z2
D=zeros(100,100,16,16);
for i=1:100
	for j=i:100
		for z1=1:16
			for z2=1:16
				 thetadiff=mod(z2-z1,16)+1;
				D(i,j,z1,z2)=C(i,j,thetadiff);
				D(j,i,z2,z1)=C(i,j,thetadiff);
    	                end
    	        end
	end
	
end
end


