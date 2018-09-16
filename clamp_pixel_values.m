%% clamp_pixel_values: gives a pixel value from [1, size(c_image)] given a u,v value
function [x,y] = clamp_pixel_values(u,v,c_image)
	[n,m,d] = size(c_image);

	f = @(x,sz) 1 + x * (sz-1);
	x = floor(f(u,m));
	y = floor(f(v,n));
