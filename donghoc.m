%% =========================================================
% DONG HOC THUAN ROBOT 3DOF
% L1 = 114 mm
% L2 = 162 mm
% L3 = 130 mm
% d1 = 250 mm
% =========================================================

clear;
clc;
close all;

% 1. THONG SO ROBOT

L1 = 114;      % mm
L2 = 162;      % mm
L3 = 130;      % mm
d1 = 250;      % mm

% 2. NHAP GOC KHOP

theta1 = input('Nhap theta1 (do): ');
theta2 = input('Nhap theta2 (do): ');
theta3 = input('Nhap theta3 (do): ');

% Doi do -> radian
t1 = deg2rad(theta1);
t2 = deg2rad(theta2);
t3 = deg2rad(theta3);

% 3. MA TRAN D-H

% Khop 1
A1 = [cos(t1)   0    sin(t1)   L1*cos(t1);
      sin(t1)   0   -cos(t1)   L1*sin(t1);
      0         1    0         d1;
      0         0    0         1];

% Khop 2
A2 = [cos(t2)  -sin(t2)   0   L2*cos(t2);
      sin(t2)   cos(t2)   0   L2*sin(t2);
      0         0         1   0;
      0         0         0   1];

% Khop 3
A3 = [cos(t3)  -sin(t3)   0   L3*cos(t3);
      sin(t3)   cos(t3)   0   L3*sin(t3);
      0         0         1   0;
      0         0         0   1];

% 4. MA TRAN BIEN DOI

T01 = A1;
T02 = A1*A2;
T03 = A1*A2*A3;

% 5. TOA DO CAC KHOP

O0 = [0;0;0];

O1 = T01(1:3,4);
O2 = T02(1:3,4);
O3 = T03(1:3,4);

% 6. IN KET QUA

fprintf('\n===== DONG HOC THUAN =====\n');

fprintf('O1  = (%.2f, %.2f, %.2f) mm\n', ...
    O1(1),O1(2),O1(3));

fprintf('O2  = (%.2f, %.2f, %.2f) mm\n', ...
    O2(1),O2(2),O2(3));

fprintf('END = (%.2f, %.2f, %.2f) mm\n', ...
    O3(1),O3(2),O3(3));

% =========================================================
% 7. VE ROBOT
% =========================================================

figure('Color','white', ...
       'Position',[100 100 1000 650]);

subplot(1,1,1);
hold on;
grid on;
box on;
axis equal;

% 8. DIEM TRUNG GIAN DE VE DE ROBOT


h = 60;

P = [0;
     0;
     h];

% 9. VE CAC KHAU

% O0 -> P
plot3([O0(1) P(1)], ...
      [O0(2) P(2)], ...
      [O0(3) P(3)], ...
      'b','LineWidth',4);

% P -> O1
plot3([P(1) O1(1)], ...
      [P(2) O1(2)], ...
      [P(3) O1(3)], ...
      'b','LineWidth',4);

% O1 -> O2
plot3([O1(1) O2(1)], ...
      [O1(2) O2(2)], ...
      [O1(3) O2(3)], ...
      'r','LineWidth',4);

% O2 -> End
plot3([O2(1) O3(1)], ...
      [O2(2) O3(2)], ...
      [O2(3) O3(3)], ...
      'g','LineWidth',4);

% 10. VE CAC KHOP

% O0
plot3(O0(1),O0(2),O0(3), ...
    'ko', ...
    'MarkerSize',9, ...
    'MarkerFaceColor','k');

% O1
plot3(O1(1),O1(2),O1(3), ...
    'bo', ...
    'MarkerSize',10, ...
    'MarkerFaceColor','b');

% O2
plot3(O2(1),O2(2),O2(3), ...
    'ro', ...
    'MarkerSize',10, ...
    'MarkerFaceColor','r');

% 11. VE DAU * TAI END-EFFECTOR

plot3(O3(1),O3(2),O3(3), ...
    'k*', ...
    'MarkerSize',14, ...
    'LineWidth',2);

% 12. GAN TEN CAC KHOP

text(O0(1),O0(2),O0(3), ...
    '  O0', ...
    'FontWeight','bold');

text(O1(1),O1(2),O1(3), ...
    '  O1', ...
    'FontWeight','bold');

text(O2(1),O2(2),O2(3), ...
    '  O2', ...
    'FontWeight','bold');

text(O3(1),O3(2),O3(3), ...
    '  END', ...
    'FontWeight','bold');

%% =========================================================
% 13. HIEN THI TOA DO TAI END-EFFECTOR
%% =========================================================

toaDo = sprintf( ...
    '(%.2f, %.2f, %.2f) mm', ...
    O3(1), O3(2), O3(3));

text(O3(1)+10, ...
     O3(2)+10, ...
     O3(3)+10, ...
     toaDo, ...
     'FontSize',10, ...
     'FontWeight','bold', ...
     'BackgroundColor','yellow', ...
     'EdgeColor','black');

%% =========================================================
% 14. VE HE TRUC XYZ TAI O0
%% =========================================================

axisLength = 100;

% Truc X
quiver3(0,0,0, ...
        axisLength,0,0, ...
        'r', ...
        'LineWidth',2, ...
        'MaxHeadSize',0.5);

% Truc Y
quiver3(0,0,0, ...
        0,axisLength,0, ...
        'g', ...
        'LineWidth',2, ...
        'MaxHeadSize',0.5);

% Truc Z
quiver3(0,0,0, ...
        0,0,axisLength, ...
        'b', ...
        'LineWidth',2, ...
        'MaxHeadSize',0.5);

%% 15. GAN TEN XYZ

text(axisLength+10,0,0, ...
    'X', ...
    'Color','r', ...
    'FontSize',12, ...
    'FontWeight','bold');

text(0,axisLength+10,0, ...
    'Y', ...
    'Color','g', ...
    'FontSize',12, ...
    'FontWeight','bold');

text(0,0,axisLength+10, ...
    'Z', ...
    'Color','b', ...
    'FontSize',12, ...
    'FontWeight','bold');

%% =========================================================
% 16. CAI DAT DO THI
%% =========================================================

xlabel('X (mm)');
ylabel('Y (mm)');
zlabel('Z (mm)');

title({ ...
    'Dong hoc thuan Robot 3DOF', ...
    sprintf('\\theta_1 = %.1f^o, \\theta_2 = %.1f^o, \\theta_3 = %.1f^o', ...
    theta1,theta2,theta3) ...
    });

xlim([-450 450]);
ylim([-450 450]);
zlim([0 500]);

view(45,25);

hold off;