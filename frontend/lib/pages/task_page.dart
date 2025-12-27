import 'package:flutter/material.dart';
import '../models/task.dart';
import '../services/api_service.dart';

class TaskPage extends StatefulWidget {
  const TaskPage({super.key});

  @override
  State<TaskPage> createState() => _TaskPageState();
}

class _TaskPageState extends State<TaskPage> {
  final titleController = TextEditingController();
  final descController = TextEditingController();

  List<Task> tasks = [];

  @override
  void initState() {
    super.initState();
    loadTasks();
  }

  Future<void> loadTasks() async {
    final fetchedTasks = await ApiService.fetchTasks();
    if (!mounted) return;
    setState(() {
      tasks = fetchedTasks;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Smart Task Manager")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: titleController,
              decoration: const InputDecoration(labelText: "Task Title"),
            ),
            TextField(
              controller: descController,
              decoration: const InputDecoration(labelText: "Task Description"),
            ),
            const SizedBox(height: 12),

            Row(
              children: [
                ElevatedButton(
                  onPressed: () async {
                    final result = await ApiService.classifyTask(
                      titleController.text,
                      descController.text,
                    );

                    if (!mounted) return;

                    showDialog(
                      context: context,
                      builder: (_) => AlertDialog(
                        title: const Text("Classification"),
                        content: Text(result.toString()),
                      ),
                    );
                  },
                  child: const Text("Classify"),
                ),
                const SizedBox(width: 10),
                ElevatedButton(
                  onPressed: () async {
                    await ApiService.createTask(
                      titleController.text,
                      descController.text,
                    );
                    titleController.clear();
                    descController.clear();
                    await loadTasks();
                  },
                  child: const Text("Create Task"),
                ),
              ],
            ),

            const SizedBox(height: 20),
            const Text("Tasks", style: TextStyle(fontSize: 18)),

            Expanded(
              child: ListView.builder(
                itemCount: tasks.length,
                itemBuilder: (_, index) {
                  final task = tasks[index];
                  return Card(
                    child: ListTile(
                      title: Text(task.title),
                      subtitle: Text(
                        "Priority: ${task.priority} | Status: ${task.status}",
                      ),
                    ),
                  );
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
