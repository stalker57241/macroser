typedef struct { int x, y; } vec2i;
typedef struct { float x, y; } vec2f;
typedef struct { double x, y; } vec2d;

typedef struct { int x, y, z; } vec3i;
typedef struct { float x, y, z; } vec3f;
typedef struct { double x, y, z; } vec3d;

typedef struct { int x, y, z, w; } vec4i;
typedef struct { float x, y, z, w; } vec4f;
typedef struct { double x, y, z, w; } vec4d;

vec2i vec2i_add(vec2i a, vec2i b) {
	return (vec2i) {
		.x = a.x + b.x,
		.y = a.y + b.y
	};
}
vec2i vec2i_sub(vec2i a, vec2i b) {
	return (vec2i) {
		.x = a.x - b.x,
		.y = a.y - b.y
	};
}
vec2f vec2f_add(vec2f a, vec2f b) {
	return (vec2f) {
		.x = a.x + b.x,
		.y = a.y + b.y
	};
}
vec2f vec2f_sub(vec2f a, vec2f b) {
	return (vec2f) {
		.x = a.x - b.x,
		.y = a.y - b.y
	};
}
vec2d vec2d_add(vec2d a, vec2d b) {
	return (vec2d) {
		.x = a.x + b.x,
		.y = a.y + b.y
	};
}
vec2d vec2d_sub(vec2d a, vec2d b) {
	return (vec2d) {
		.x = a.x - b.x,
		.y = a.y - b.y
	};
}

vec3i vec3i_add(vec3i a, vec3i b) {
	return (vec3i) {
		.x = a.x + b.x,
		.y = a.y + b.y,
		.z = a.z + b.z
	};
}
vec3i vec3i_sub(vec3i a, vec3i b) {
	return (vec3i) {
		.x = a.x - b.x,
		.y = a.y - b.y,
		.z = a.z - b.z
	};
}
vec3f vec3f_add(vec3f a, vec3f b) {
	return (vec3f) {
		.x = a.x + b.x,
		.y = a.y + b.y,
		.z = a.z + b.z
	};
}
vec3f vec3f_sub(vec3f a, vec3f b) {
	return (vec3f) {
		.x = a.x - b.x,
		.y = a.y - b.y,
		.z = a.z - b.z
	};
}
vec3d vec3d_add(vec3d a, vec3d b) {
	return (vec3d) {
		.x = a.x + b.x,
		.y = a.y + b.y,
		.z = a.z + b.z
	};
}
vec3d vec3d_sub(vec3d a, vec3d b) {
	return (vec3d) {
		.x = a.x - b.x,
		.y = a.y - b.y,
		.z = a.z - b.z
	};
}

vec4i vec4i_add(vec4i a, vec4i b) {
	return (vec4i) {
		.x = a.x + b.x,
		.y = a.y + b.y,
		.z = a.z + b.z,
		.w = a.w + b.w
	};
}
vec4i vec4i_sub(vec4i a, vec4i b) {
	return (vec4i) {
		.x = a.x - b.x,
		.y = a.y - b.y,
		.z = a.z - b.z,
		.w = a.w - b.w
	};
}
vec4f vec4f_add(vec4f a, vec4f b) {
	return (vec4f) {
		.x = a.x + b.x,
		.y = a.y + b.y,
		.z = a.z + b.z,
		.w = a.w + b.w
	};
}
vec4f vec4f_sub(vec4f a, vec4f b) {
	return (vec4f) {
		.x = a.x - b.x,
		.y = a.y - b.y,
		.z = a.z - b.z,
		.w = a.w - b.w
	};
}
vec4d vec4d_add(vec4d a, vec4d b) {
	return (vec4d) {
		.x = a.x + b.x,
		.y = a.y + b.y,
		.z = a.z + b.z,
		.w = a.w + b.w
	};
}
vec4d vec4d_sub(vec4d a, vec4d b) {
	return (vec4d) {
		.x = a.x - b.x,
		.y = a.y - b.y,
		.z = a.z - b.z,
		.w = a.w - b.w
	};
}

int main() {
    return 0;
}