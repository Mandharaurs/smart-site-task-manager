class Task {
  final String id; // ✅ UUID is STRING
  final String title;
  final String description;
  final String priority;
  final String status;

  Task({
    required this.id,
    required this.title,
    required this.description,
    required this.priority,
    required this.status,
  });

  factory Task.fromJson(Map<String, dynamic> json) {
    return Task(
      id: json["id"].toString(), // ✅ safe conversion
      title: json["title"],
      description: json["description"] ?? "",
      priority: json["priority"],
      status: json["status"],
    );
  }
}
