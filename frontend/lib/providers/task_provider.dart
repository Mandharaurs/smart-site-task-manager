import 'package:flutter/material.dart';
import '../models/task.dart';
import '../services/api_service.dart';

class TaskProvider extends ChangeNotifier {
  List<Task> tasks = [];
  bool loading = false;

  // 🔹 Fetch all tasks
  Future<void> fetchTasks() async {
    loading = true;
    notifyListeners();

    try {
      tasks = await ApiService.fetchTasks();
    } catch (e) {
      debugPrint("Fetch tasks error: $e");
    }

    loading = false;
    notifyListeners();
  }

  // 🔹 Create a new task
  Future<void> createTask({
    required String title,
    required String description,
    required String category,
    required String priority,
  }) async {
    try {
      await ApiService.createTask(
        title,
        description,
        category,
        priority,
      );

      await fetchTasks(); // refresh list
    } catch (e) {
      debugPrint("Create task error: $e");
    }
  }

  // ===============================
  // ✅ DASHBOARD GETTERS (FIX)
  // ===============================

  /// Tasks that are NOT completed
  int get pendingCount {
    return tasks.where((t) => t.completed == false).length;
  }

  /// Tasks that ARE completed
  int get completedCount {
    return tasks.where((t) => t.completed == true).length;
  }
}
