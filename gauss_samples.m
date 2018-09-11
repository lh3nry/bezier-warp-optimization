% gauss_test.m
%% gauss_samples: Samples n pixels (per control point) in an image of size im_width 
				% about control points [Cx,Cy]
function [r_samples] = gauss_samples(Cx,Cy,im_width,tightness,pad,num_samples)
% num_samples = 10;
% tightness = im_width/4;

points = [Cx Cy];


sigma = tightness * eye(2);

r_samples = [];

for i = 1:length(points)
	mu = [points(i,1) points(i,2)];
	% mu = points(i);
	r_samples = [r_samples; floor(mvnrnd(mu,sigma,num_samples))];
end

