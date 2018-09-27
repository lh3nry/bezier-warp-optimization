% projector_ray.m
%% projector_ray: generates the rays from the projector origin
function out = projector_ray(p_origin, proj, u,v)
	out = bilinear_interp(proj,u,v);
