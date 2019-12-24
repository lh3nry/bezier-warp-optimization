h = figure(1);
hold on;
axis vis3d
set(h, 'Position', [1200 500 750 750]);
xlabel('x'); ylabel('y'); zlabel('z');
grid;
shading interp
view(-35,15);