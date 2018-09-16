% projector_ray.m
%% projector_ray: generates the rays from the projector origin
function out = projector_ray(p_origin, proj, x,y, c_image)
	u = floor(x/size(c_image,1));
	v = floor(y/size(c_image,2));
	xy = floor([x y]);
	color_out = reshape(c_image(xy(1),xy(2),:),1,3);

	direction = bilinear_interp(proj,u,v) - p_origin;
	out = [direction color_out];