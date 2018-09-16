% projector_ray.m
%% projector_ray: generates the rays from the projector origin
function out = projector_ray(p_origin, proj, u,v, c_image)
	% x = u*size(c_image,1);
	% y = v*size(c_image,2);
	% xy = floor([x y]);
	% color_out = reshape(c_image(xy(1),xy(2),:),1,3);

	direction = bilinear_interp(proj,u,v);
	out = direction;

% %% clamp_pixel_values: function description
% function [x,y] = clamp_pixel_values(u,v,c_image)
% 	[n,m,d] = size(c_image);
% 	x = ;
% 	y = ;
