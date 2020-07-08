
struct slam_obj
{
	int id;
	std::string name;

	tf::Quaternion r;
	tf::Vector3 t;

	slam_obj *left;
	slam_obj *right;
};


class slam_tree
{
	slam_obj* root;
	slam_obj* add_(slam_obj*, slam_obj*);
	slam_obj* search_id_(slam_obj*, int);

public:
	slam_tree();
	void add(slam_obj*);
	slam_obj* search_id(int);
};

slam_tree::slam_tree()
{
	root = NULL;
}


void slam_tree::add(slam_obj* obj)
{
	root = add_(root, obj);
}

slam_obj* slam_tree::search_id(int id)
{
	return search_id_(root, id);
}


slam_obj* slam_tree::add_(slam_obj* root, slam_obj* new_object){

	if(root == NULL) return new_object;

	if(new_object->id > root->id) root->right = add_(root->right, new_object);

	else root->left = add_(root->left, new_object);

	return root;
}

slam_obj* slam_tree::search_id_(slam_obj* root, int id){

	if(root == NULL) return root;

	if(root->id == id) return root;

	if(root->id > id) return search_id_(root->left, id);

	else return search_id_(root->right, id);
}
