% projector_ray.m
%% projector_ray: generates the rays from the projector origin
function [color, direction] = projector_ray(p_origin, u,v, image)
	color = zeros(0,0,0);
	direction = zeros(0,0,0);
