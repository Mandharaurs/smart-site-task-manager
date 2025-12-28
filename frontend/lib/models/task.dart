class Task {
  final String id;
  final String title;
  final String description;
  final String category;
  final String priority;
  final bool completed;

  Task({
    required this.id,
    required this.title,
    required this.description,
    required this.category,
    required this.priority,
    required this.completed,
  });

  factory Task.fromJson(Map<String, dynamic> json) {
    return Task(
      id: json['id'],
      title: json['title'],
      description: json['description'],
      category: json['category'],
      priority: json['priority'],
      completed: json['completed'] ?? false,
    );
  }
}
