import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';

class ApiClient {
  static final Dio dio = Dio(
    BaseOptions(
      baseUrl: "https://smart-site-task-manager-backend-62bj.onrender.com",
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 10),
    ),
  )
    ..interceptors.add(
      InterceptorsWrapper(
        onRequest: (req, handler) {
          if (kDebugMode) {
            debugPrint("➡️ ${req.method} ${req.path}");
          }
          return handler.next(req);
        },
        onError: (e, handler) {
          if (kDebugMode) {
            debugPrint("❌ ${e.message}");
          }
          return handler.next(e);
        },
      ),
    );
}
