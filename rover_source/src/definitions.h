#include <iostream>
#include <cmath>

using namespace std;

const double PI = 3.14159265;
const double TOLERANCE = 0.1;

double abs_val(double candidate){

	if(candidate < 0) return candidate*(-1);
	return candidate;
}

class coordinate{

	double x;
	double y;
	double z;

public:

	coordinate(double = 0.0, double = 0.0, double = 0.0);
	void set_x(double);
	void set_y(double);
	void set_z(double);
	double get_x();
	double get_y();
	double get_z();
	void update(double, double, double);
	double calculate_dist(coordinate);
	coordinate crd_multiplication(double);
	coordinate operator+(coordinate);
};

coordinate::coordinate(double crd_x, double crd_y, double crd_z){

	x = crd_x;
	y = crd_y;
	z = crd_z;
}

void coordinate::set_x(double new_x){

	x = new_x;
}

void coordinate::set_y(double new_y){

	y = new_y;
}

void coordinate::set_z(double new_z){

	z = new_z;
}

double coordinate::get_x(){

	return x;
}

double coordinate::get_y(){

	return y;
}

double coordinate::get_z(){

	return z;
}

void coordinate::update(double new_x, double new_y, double new_z){

	x += new_x;
	y += new_y;
	z += new_z;
}

double coordinate::calculate_dist(coordinate second_cord){

	double x_dist = second_cord.get_x() - x;
	double y_dist = second_cord.get_y() - y;
	double z_dist = second_cord.get_z() - z;

	return sqrt(x_dist*x_dist + y_dist*y_dist + z_dist*z_dist);
}

coordinate coordinate::crd_multiplication(double factor){

	double new_x = factor*x;
	double new_y = factor*y;
	double new_z = factor*z;

	return coordinate(new_x, new_y, new_z);
}

coordinate coordinate::operator+(coordinate to_be_added){

	double new_x = (this->get_x()) + to_be_added.get_x();
	double new_y = (this->get_y()) + to_be_added.get_y();
	double new_z = (this->get_z()) + to_be_added.get_z();

	return coordinate(new_x, new_y, new_z);
}


double dot_product(coordinate one, coordinate two){

	int i;
	double result = 0.0;

	result += one.get_x() * two.get_x();
	result += one.get_y() * two.get_y();
	result += one.get_z() * two.get_z();

	return result;
}

double angle_of_vectors(coordinate one, coordinate two){

	coordinate base_coord = coordinate(0,0,0);

	double magnitude_one = one.calculate_dist(base_coord);
	double magnitude_two = two.calculate_dist(base_coord);

	double angle = (acos(dot_product(one,two)/(magnitude_one*magnitude_two))*180)/PI;

	return angle;
}

double find_angle(coordinate center, coordinate before, coordinate next){

	double a = center.calculate_dist(before);
	double b = center.calculate_dist(next);
	double c = before.calculate_dist(next); 

	double my_angle = (acos((a*a + b*b - c*c)/(2*a*b))*180)/PI;

	coordinate new_before = coordinate(before.get_x()-center.get_x(), before.get_y()-center.get_y(), before.get_z()-center.get_z());
	coordinate new_next = coordinate(next.get_x()-center.get_x(), next.get_y()-center.get_y(), next.get_z()-center.get_z());

	double cross_product_y = new_before.get_z()*new_next.get_x() - new_before.get_x()*new_next.get_z();

	if(cross_product_y > 0)  my_angle = 360 - my_angle;

	return my_angle;
}

double cosinus_theorem(coordinate center, coordinate one, coordinate two){

	double a = center.calculate_dist(one);
	double b = center.calculate_dist(two);
	double c = one.calculate_dist(two); 

	double my_angle = (acos((a*a + b*b - c*c)/(2*a*b))*180)/PI;

	return my_angle;
}

void rotate_on_xy(coordinate& to_be_rotated, double angle){

	double angle_radian = (angle*PI)/180;

	double new_x = to_be_rotated.get_x()*cos(angle_radian) - to_be_rotated.get_y()*sin(angle_radian);		// Rotation matrix is used
	double new_y = to_be_rotated.get_x()*sin(angle_radian) + to_be_rotated.get_y()*cos(angle_radian);

	to_be_rotated.set_x(new_x);
	to_be_rotated.set_y(new_y);
}

class joy_message{

	double axes[6];
	double buttons[12];

public:

	void set_axes(double,double,double,double,double,double);
	double get_axis(int);
	void set_buttons(double,double,double,double,double,double,double,double,double,double,double,double);
	double get_button(int);
};

void joy_message::set_axes(double new_axis_0, double new_axis_1, double new_axis_2, double new_axis_3, double new_axis_4, double new_axis_5){

	axes[0] = new_axis_0;
	axes[1] = new_axis_1;
	axes[2] = new_axis_2;
	axes[3] = new_axis_3;
	axes[4] = new_axis_4;
	axes[5] = new_axis_5;
}

double joy_message::get_axis(int axis_index){

	return axes[axis_index];
}

void joy_message::set_buttons(double new_button_0, double new_button_1, double new_button_2, double new_button_3, double new_button_4, double new_button_5, double new_button_6, double new_button_7, double new_button_8, double new_button_9, double new_button_10, double new_button_11){

	buttons[0] = new_button_0;
	buttons[1] = new_button_1;
	buttons[2] = new_button_2;
	buttons[3] = new_button_3;
	buttons[4] = new_button_4;
	buttons[5] = new_button_5;
	buttons[6] = new_button_6;
	buttons[7] = new_button_7;
	buttons[8] = new_button_8;
	buttons[9] = new_button_9;
	buttons[10] = new_button_10;
	buttons[11] = new_button_11;
}

double joy_message::get_button(int button_index){

	return buttons[button_index];
}

void FABRIK_algorithm(vector<coordinate>& my_joints, double* link_lengths, coordinate new_end_point_pos, double REACH){

	int i;
	double r, lambda;
	double distance_from_beginning = abs_val(new_end_point_pos.calculate_dist(my_joints[0]));

	if(distance_from_beginning > REACH){

		for(i = 0; i < my_joints.size(); i++){

			r = abs_val(new_end_point_pos.calculate_dist(my_joints[i]));
			lambda = link_lengths[i]/r;

			my_joints[i+1] = my_joints[i].crd_multiplication(1-lambda) + new_end_point_pos.crd_multiplication(lambda);
		}

	}

	else{

		coordinate b;
		b = my_joints[0];

		double distance_to_target = new_end_point_pos.calculate_dist(my_joints[my_joints.size()-1]);

		while(distance_to_target > TOLERANCE){

			my_joints[my_joints.size()-1] = new_end_point_pos;

			for(i = my_joints.size()-2; i >= 0; i--){

				r = abs_val(my_joints[i+1].calculate_dist(my_joints[i]));
				lambda = link_lengths[i]/r;

				my_joints[i] = my_joints[i+1].crd_multiplication(1-lambda) + my_joints[i].crd_multiplication(lambda);
			}

			my_joints[0] = b;

			for(i = 0; i < my_joints.size()-1; i++){

				r = abs_val(my_joints[i+1].calculate_dist(my_joints[i]));
				lambda = link_lengths[i]/r;

				my_joints[i+1] = my_joints[i].crd_multiplication(1-lambda) + my_joints[i+1].crd_multiplication(lambda); 
			}

			distance_to_target = abs_val(my_joints[my_joints.size()-1].calculate_dist(new_end_point_pos));
		}
	}
}