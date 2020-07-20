
/*
	Main data structure of slam system
*/
struct slam_obj
{
	int id, relocalization_cooldown_counter;
	std::string name;

	tf::Quaternion R;
	tf::Vector3 T;

	slam_obj *left;
	slam_obj *right;
};

/*
	Interface class between algorithm and data structure
*/
class slam_tree
{
	slam_obj* root;
	slam_obj* add_(slam_obj*, slam_obj*);
	slam_obj* search_id_(slam_obj*, int);
	void traverse_(slam_obj*, tf::TransformBroadcaster, void (*action)(tf::TransformBroadcaster, slam_obj*));

public:
	slam_tree();
	void add(slam_obj*);
	void traverse(tf::TransformBroadcaster, void (*action)(tf::TransformBroadcaster, slam_obj*));
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

void slam_tree::traverse(tf::TransformBroadcaster br, void (*action)(tf::TransformBroadcaster br, slam_obj *obj))
{
	traverse_(root, br, action);
}

void slam_tree::traverse_(slam_obj* root, tf::TransformBroadcaster br, void (*action)(tf::TransformBroadcaster br, slam_obj *obj))
{
	if(root->right != NULL)
		traverse_(root->right, br, action);

	action(br, root);

	if(root->left != NULL)
		traverse_(root->left, br, action);
}
