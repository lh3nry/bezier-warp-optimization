% bilinear_interp.m
%% bilinear_interp: bilinear interpolation of a plane in 3D space
function [x] = bilinear_interp(A,u,v)
	x = zeros(1,3);
	for i = 1:3
		G = [A(4,i) A(3,i);A(2,i) A(1,i)];
		x(i) = [1-u u] * G *[1-v ; v];
	end
	% x = A(4,:) * (1-u)*(1-v)	...
	%   + A(2,:) * (1-v)*u 		...
	%   + A(3,:) * (1-u)*v 		...
	%   + A(1,:) * u*v;
