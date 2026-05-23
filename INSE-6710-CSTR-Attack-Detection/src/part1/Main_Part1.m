clear all
close all
clc

%associated simulink file name
file_simulink='NetworkedControlSystemBasic.slx';

%   ***Model of the Industrial Continuous-Stirred Tank Reactor (CSTR) system 
A=[0.9719 -0.0013;-0.0340 0.8628];
B=[-0.0839 0.0232;0.0761 0.4144];
C=[0 1];
D=[0 0];

Ts=1;%Sampling Time
standardDeviationProcessNoise=0.007;
Q=(standardDeviationProcessNoise)^2*eye(size(A,1)); %covariance process noise
standardDeviationMeasurementNoise=0.04;
R=(standardDeviationMeasurementNoise)^2*eye(size(C,1));% covariance measurement noise
% controller configuration
Q_LQI=[0.1 0 0;0 0.1 0; 0 0 1];%*eye(size(A,1)+size(C,1)); % LQ desired cost matrix for the state 
R_LQ=100*eye(size(B,2)); % LQ desired cost matrix for the input 
Tsim=400;

% reference signal configuration
reference_value_vec=[0 10 17]; % desired sequence of value for the output
reference_time_vec=[0 100 250];% time instants at which each element of the reference is activated (one to one correspondance)

%   ***properties***
fprintf('Checking necessary properties for control design: ');
if rank(ctrb(A,B))~=size(A,2)
    error('system not controllable')
else
    fprintf('system is controllable ')
end
if rank(obsv(A,C))~=size(A,2)
    error('system not observable')
else
    fprintf('and observable\n')
end

%   ***Controller Design***
fprintf('Controller Design....\n');
%state space representation
sys=ss(A,B,C,D,Ts);
%LQI controller for piece-wise reference tracking: K=[K1, K2]
K=lqi(sys,Q_LQI,R_LQ,0);
% 

%	***Kalman state Estimato Design***
%x[n+1]=Ax[n]+Bu[n]+Gw[n]
%y[n]=Cx[n]+Du[n]+Hw[n]+v[n]
fprintf('Steady-state Kalman filter design....\n');
G=eye(length(A)); %<--this says that the process noise affect all the state components
H=zeros(size(C,1),length(A));%<--this says tha the process noise does not affect the output 
% (only the sensor measurements affect the output)
SYS=ss(A,[B G],C,[D H],Ts);
[KEST,L,P]=kalman(SYS,Q,R);

% stability test using the controller K1
eig_controller=eig(A-B*K(:,1:size(A,1)));
for i=1:length(eig_controller)
    if abs(eig_controller(i))>0.999999999
        error('The closed-loop system is not asympt. stable')
    end
end
fprintf('The closed-loop system is asympt. stable\n');

% stability test for the state estimator using L obtained from the Kalman
% filter
eig_estimator=eig(A-L*C);
for i=1:length(eig_estimator)
    if abs(eig_estimator(i))>0.999999999
        error('The state estimator is not asympt stable\n')
    end
end
fprintf('The state estimator is asympt stable\n');

fprintf('Designed Parameters:\n');
% Designed Parameters
K, L, P 

%  ***Simulation Initialization
x0=zeros(size(A,1),1);
%x0_hat=zeros(size(A,1),1);
x0_hat=zeros(size(A,1),1);

%the command "sim" allows you to run the simulink file from Matlab

num_trials = 50;
Tsim = 400;
Ts = 1;
N_steps = Tsim / Ts;

FP = 0;
TN = 0;
Je_total = 0;

fprintf('\nRunning %d trials...\n', num_trials);

for trial = 1:num_trials
    % Run simulation
    output = sim(file_simulink);

    % Extract time and output signal
    y_seq = output.y.signals.values;
    result_seq = output.detector_outcome.signals.values;
    time_seq = output.y.time;

    % Generate reference signal
    ref_seq = zeros(size(y_seq));
    for i = 1:length(time_seq)
        t = time_seq(i);
        if t < 100
            ref_seq(i) = 0;
        elseif t < 250
            ref_seq(i) = 10;
        else
            ref_seq(i) = 17;
        end
    end

    % Count FP and TN (we are in no-attack case)
    FP = FP + sum(result_seq == 1);
    TN = TN + sum(result_seq == 0);

    % Tracking error Je = average squared error
    Je_total = Je_total + sum((y_seq - ref_seq).^2) / N_steps;
end

% Average Je over trials
Je_avg = Je_total / num_trials;

% Compute false alarm rate
falarm = 100 * FP / (FP + TN);

% Show results
fprintf('\n--- PART 1 RESULTS ---\n');
fprintf('False Positives (FP): %d\n', FP);
fprintf('True Negatives (TN): %d\n', TN);
fprintf('False Alarm Rate: %.2f%%\n', falarm);
fprintf('Average Tracking Error Je: %.4f\n', Je_avg);

% Store results in a table
results = table(FP, TN, falarm, Je_avg, ...
    'VariableNames', {'FP', 'TN', 'falarm_percent', 'Je'});
disp(results);

%% One More Simulation for Plotting
fprintf('\nRunning one clean trial to generate plots...\n');
output = sim(file_simulink);

% Time
time_seq = output.y.time;
Tsim = length(time_seq);
Ts = 1;

% Signals
y_seq = output.y.signals.values;
u_seq = output.u.signals.values;
x_seq = output.x.signals.values;
x_hat_seq = output.x_hat.signals.values;

% Reference signal
ref_seq = zeros(size(y_seq));
for i = 1:length(time_seq)
    t = time_seq(i);
    if t < 100
        ref_seq(i) = 0;
    elseif t < 250
        ref_seq(i) = 10;
    else
        ref_seq(i) = 17;
    end
end

widthline = 2;  % Line width setting for all plots

%% Generate Reference Signal for Plot
time_to_plot = 0:Ts:Tsim - Ts;
reference_to_plot = zeros(size(C,1), length(time_to_plot));
index = 1;
for i = 1:length(time_to_plot)
    T_curr = i * Ts;
    if index < length(reference_value_vec) && T_curr >= reference_time_vec(index+1)
        index = index + 1;
    end
    reference_to_plot(:,i) = reference_value_vec(:,index);
end

%% Plot 1: Sensor Output y vs Reference
y_seq = output.y.signals.values;
time_seq = output.y.time;
figure
for i = 1:size(y_seq,2)
    subplot(size(y_seq,2), 1, i);
    plot(time_seq, y_seq(:,i), 'b', 'LineWidth', widthline)
    hold on
    plot(time_to_plot, reference_to_plot(i,:), 'r--', 'LineWidth', widthline)
    grid on
    title(sprintf('Output %i', i))
    xlabel('time [sec]')
    ylabel(sprintf('y%i', i))
    legend('Output','Reference')
end

%% Plot 2: Control Inputs u
u_seq = output.u.signals.values;
time_seq = output.u.time;
figure
for i = 1:size(u_seq,2)
    subplot(size(u_seq,2),1,i);
    plot(time_seq, u_seq(:,i), 'b', 'LineWidth', widthline)
    grid on
    title(sprintf('Control Input %i', i))
    xlabel('time [sec]')
    ylabel(sprintf('u%i', i))
end

%% Plot 3: Real State x vs Estimated State x_hat
x_seq = output.x.signals.values;
x_hat_seq = output.x_hat.signals.values;
time_seq = output.x.time;
figure
for i = 1:size(x_seq,2)
    subplot(size(x_seq,2), 1, i);
    plot(time_seq, x_seq(:,i), 'b', 'LineWidth', widthline)
    hold on
    plot(time_seq, x_hat_seq(:,i), 'r--', 'LineWidth', widthline)
    grid on
    title(sprintf('State %i', i))
    xlabel('time [sec]')
    ylabel(sprintf('x%i', i))
    legend('Real', 'Estimated')
end

%% Plot 4: Chi-squared Test Statistic z(k)
alpha = 0.03; v = 1;
tau = chi2inv(1 - alpha, v);
figure
plot(z_log, 'r', 'LineWidth', widthline)
hold on
yline(tau, 'k--', 'LineWidth', widthline)
xlabel('Time step k')
ylabel('z(k)')
title(sprintf('Chi-squared Test Statistic vs Threshold (\\tau = %.4f)', tau))
legend('z(k)', sprintf('\\tau = %.4f', tau))
grid on

%% Set Calibri font and size for all plots
fh = findall(0,'Type','Figure');
txt_obj = findall(fh,'Type','text');
set(txt_obj,'FontName','Calibri','FontSize',15);

