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

