% projector_ray.m
%% projector_ray: generates the rays from the projector origin
function [color, direction] = projector_ray(p_origin, proj, x,y, c_image)
	u = floor(x/size(c_image,1));
	v = floor(y/size(c_image,2));
	color = c_image(x,y,:);
	direction = bilinear_interp(proj,u,v) - p_origin;
