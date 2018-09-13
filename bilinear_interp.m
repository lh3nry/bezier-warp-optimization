% bilinear_interp.m
%% bilinear_interp: bilinear interpolation of a plane in 3D space
function [x] = bilinear_interp(A,u,v)
	x = zeros(1,3);
	for i = 1:3
		G = [A(1,i) A(2,i) ; A(3,i) A(4,i)];
		x(i) = [1-u u] * G *[1-v ; v];
	end

