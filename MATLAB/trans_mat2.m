% trans_mat2.m
%% trans_mat2: Translates all points in P (Nx3)
%% possibly faster with the use of bsxfun
function [P_] = trans_mat2(P,x,y,z)
	P_ = bsxfun(@plus,P,[x y z]);
