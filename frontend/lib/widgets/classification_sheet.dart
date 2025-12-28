import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/task_provider.dart';
import '../services/api_service.dart';

class ClassificationSheet extends StatelessWidget {
  final String title;
  final String description;

  const ClassificationSheet({
    super.key,
    required this.title,
    required this.description,
  });

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<Map<String, dynamic>>(
      future: ApiService.classifyTask(title, description),
      builder: (context, snapshot) {
        if (!snapshot.hasData) {
          return const Padding(
            padding: EdgeInsets.all(32),
            child: Center(child: CircularProgressIndicator()),
          );
        }

        final analysis = snapshot.data!;
        final category = analysis['category'];
        final priority = analysis['priority'];

        return Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text(
                "Auto Classification",
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 12),
              Text("Category: $category"),
              Text("Priority: ${priority.toUpperCase()}"),
              const SizedBox(height: 24),
              Align(
                alignment: Alignment.centerRight,
                child: ElevatedButton(
                  child: const Text("Save Task"),
                  onPressed: () async {
                    final provider = context.read<TaskProvider>();

                    await provider.createTask(
                          title: title,
                          description: description,
                          category: category,
                          priority: priority,
                        );
                    
                    if(context.mounted){
                    Navigator.pop(context);
                    }
                  },
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
