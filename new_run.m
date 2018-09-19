% new_run.m


close all;
clear all;

preview_cam

scene

im = imread('colour_test.png');

% figure(2);
% imshow(im);


P = proj_plane(1:4,:);

[rays, plt] = spawn_rays(10,10,P,o);


figure(1);
hold on;

plot3(plt(:,1),plt(:,2),plt(:,3),'g');
plot3(P(:,1),P(:,2),P(:,3),'b*');

bvh = [max([x y z]) ; min([x y z])]

line(bvh(:,1),[0;0],[0;0])
line(bvh(:,1),repmat(max(y),2,1),[0;0])
line([0;0],[0;0],bvh(:,3))
line([0;0],repmat(max(y),2,1),bvh(:,3))

N = [0 0 bvh(1,3)];
E = [bvh(1,1) 0 0];
S = -N;
W = -E;
NW = [bvh(2,1) 0 bvh(1,3)];
SW = [bvh(2,1) 0 bvh(2,3)];
SE = -NW; %[bvh(1,1) 0 bvh(2,3)];
NE = -SW; %[bvh(1,1) 0 bvh(1,3)];
OO = zeros(1,3);

plot_quad(1,N,NE,OO,E,'g');
plot_quad(1,NW,N,W,OO,'r');
plot_quad(1,W,OO,SW,S,'g');
plot_quad(1,OO,E,S,SE,'r');