% Mô phỏng động học nghịch
clear;
clc;
close all;

% 1. THONG SO ROBOT (mm)
L1 = 114;
L2 = 162;
L3 = 130;
d1 = 250;

%Nhập toạ độ mục tiêu
Px=input('Nhập Px(mm): ');
Py=input('Nhập Py(mm): ');
Pz=input('Nhập Pz(mm): ');

% Tính động học nghịch
theta1 = atan2(Py,Px);

Z = Pz - d1;
R = sqrt((Px^2 + Py^2))-L1;
D = (Z^2 + R^2 - L2^2 -L3^2)/(2*L2*L3);
% theta3 có 2 nghiệm
theta3_1 = atan2(sqrt(1-D^2),D);
theta3_2 = atan2(-sqrt(1-D^2),D);

% tính theta2 theo 2 nghiệm của theta3
A1 = L2 + L3*cos(theta3_1);
B1 = L3*sin(theta3_1);
A2 = L2 + L3*cos(theta3_2);
B2 = L3*sin(theta3_2);

theta2_1 = atan2((A1*Z - B1*R),(B1*Z + A1*R));
theta2_2 = atan2((A2*Z - B2*R),(B2*Z + A2*R));

%% 4. HIEN THI GOC KHOP

fprintf('\n===== NGHIEM 1 =====\n');
fprintf('Theta1 = %.2f do\n',rad2deg(theta1));
fprintf('Theta2 = %.2f do\n',rad2deg(theta2_1));
fprintf('Theta3 = %.2f do\n',rad2deg(theta3_1));

fprintf('\n===== NGHIEM 2 =====\n');
fprintf('Theta1 = %.2f do\n',rad2deg(theta1));
fprintf('Theta2 = %.2f do\n',rad2deg(theta2_2));
fprintf('Theta3 = %.2f do\n',rad2deg(theta3_2));

%% 5. VE ROBOT CHO HAI NGHIEM

theta2_all = [theta2_1,theta2_2];
theta3_all = [theta3_1,theta3_2];

figure('Color','white', ...
       'Position',[100 100 1400 650]);

for k = 1:2

    t2 = theta2_all(k);
    t3 = theta3_all(k);

    %% 6. TOA DO CAC KHOP

    O0 = [0;0;0];

    O1 = [L1*cos(theta1);
          L1*sin(theta1);
          d1];

    O2 = [(L1+L2*cos(t2))*cos(theta1);
          (L1+L2*cos(t2))*sin(theta1);
          d1+L2*sin(t2)];

    O3 = [(L1+L2*cos(t2)+L3*cos(t2+t3))*cos(theta1);
          (L1+L2*cos(t2)+L3*cos(t2+t3))*sin(theta1);
          d1+L2*sin(t2)+L3*sin(t2+t3)];

    % Kiem tra sai so
    saiSo = norm(O3-[Px;Py;Pz]);

    fprintf('\nSai so nghiem %d: %.8f mm\n',k,saiSo);

    %% 7. TAO DO THI

    subplot(1,2,k);
    hold on;
    grid on;
    box on;
    axis equal;

    % Diem trung gian de ve de robot
    h = 60;
    
    P = [0;
         0;
         h];

    %% 8. VE CAC KHAU

    % Ve tu O0 den P
    plot3([O0(1) P(1)], ...
          [O0(2) P(2)], ...
          [O0(3) P(3)], ...
          'b','LineWidth',4);
    
    % Ve tu P den O1
    plot3([P(1) O1(1)], ...
          [P(2) O1(2)], ...
          [P(3) O1(3)], ...
          'b','LineWidth',4);

    % Khau 2
    plot3([O1(1) O2(1)], ...
          [O1(2) O2(2)], ...
          [O1(3) O2(3)], ...
          'r','LineWidth',4);

    % Khau 3
    plot3([O2(1) O3(1)], ...
          [O2(2) O3(2)], ...
          [O2(3) O3(3)], ...
          'g','LineWidth',4);

    %% 9. VE CAC KHOP

    plot3(O0(1),O0(2),O0(3), ...
          'ko','MarkerSize',9, ...
          'MarkerFaceColor','k');

    plot3(O1(1),O1(2),O1(3), ...
          'bo','MarkerSize',10, ...
          'MarkerFaceColor','b');

    plot3(O2(1),O2(2),O2(3), ...
          'ro','MarkerSize',10, ...
          'MarkerFaceColor','r');

    % Dau * tai End-Effector
    plot3(O3(1),O3(2),O3(3), ...
          'k*','MarkerSize',14, ...
          'LineWidth',2);

    %% 10. GAN TEN CAC KHOP

    text(O0(1),O0(2),O0(3), ...
         ' O0','FontWeight','bold');

    text(O1(1),O1(2),O1(3), ...
         ' O1','FontWeight','bold');

    text(O2(1),O2(2),O2(3), ...
         ' O2','FontWeight','bold');

    text(O3(1),O3(2),O3(3), ...
         ' END','FontWeight','bold');

    %% 11. HIEN THI TOA DO END-EFFECTOR

    toaDo = sprintf('(%.2f, %.2f, %.2f) mm', ...
                    O3(1),O3(2),O3(3));

    % Dat o toa do gan End-Effector
    text(O3(1)+10, ...
         O3(2)+10, ...
         O3(3)+10, ...
         toaDo, ...
         'FontSize',10, ...
         'FontWeight','bold', ...
         'BackgroundColor','yellow', ...
         'EdgeColor','black', ...
         'Margin',4, ...
         'Clipping','off');

    %% 12. VE HE TRUC XYZ

    axisLength = 100;

    % Truc X
    quiver3(0,0,0,axisLength,0,0, ...
            'r','LineWidth',2, ...
            'MaxHeadSize',0.5);

    % Truc Y
    quiver3(0,0,0,0,axisLength,0, ...
            'g','LineWidth',2, ...
            'MaxHeadSize',0.5);

    % Truc Z
    quiver3(0,0,0,0,0,axisLength, ...
            'b','LineWidth',2, ...
            'MaxHeadSize',0.5);

    %% 13. GAN TEN XYZ

    text(axisLength+10,0,0,'X', ...
         'Color','r','FontWeight','bold');

    text(0,axisLength+10,0,'Y', ...
         'Color','g','FontWeight','bold');

    text(0,0,axisLength+10,'Z', ...
         'Color','b','FontWeight','bold');

    %% 14. CAI DAT DO THI

    xlabel('X (mm)');
    ylabel('Y (mm)');
    zlabel('Z (mm)');

    title({sprintf('Dong hoc nghich - Nghiem %d',k), ...
           sprintf('theta1 = %.1f, theta2 = %.1f, theta3 = %.1f', ...
           rad2deg(theta1),rad2deg(t2),rad2deg(t3))});

    xlim([-550 550]);
    ylim([-550 550]);
    zlim([-100 600]);

    view(45,25);

    hold off;
end