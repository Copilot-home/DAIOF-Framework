# Tham Chiếu Độ Chính Xác Lỗi (Error Precision Reference)

## Tổng quan
Tài liệu này định nghĩa khái niệm "Lỗi" (Error) như một tham chiếu bắt buộc cho tất cả AI coding agents trên VSCode DAIOF Framework. Độ chính xác phải đạt tới giới hạn phần cứng (Floating Point Epsilon).

## Khái niệm Lỗi (Error Locking)
- **Định nghĩa**: Lỗi là sự sai lệch giữa kết quả tính toán và giá trị chân lý.
- **Giới hạn**: 1.1102230246251565e-16 (Floating Point Epsilon của máy tính).
- **Quy tắc**: Error = 0.0 hoặc ≈ 1.11e-16 là tiêu chuẩn chính xác bắt buộc.
- **Nguyên tắc**: Không được làm tròn số (rounding) nếu không có lệnh. Code phải khớp tuyệt đối với dữ liệu chân lý.

## Quy trình Kiểm tra Độ Chính Xác

### 1. Phân rã Dữ liệu (Deconstruction)
- **AI chịu trách nhiệm**: AI Kernel hoặc AI Phân tích
- **Nhiệm vụ**: So sánh kết quả với results.csv
- **Công thức**: Error = |calculated - truth| ≤ 1.1102230246251565e-16
- **Đầu ra**: Báo cáo độ chính xác

### 2. Tiến hóa Độ Chính Xác (Evolution)
- **AI chịu trách nhiệm**: AI Growth hoặc AI Học tập
- **Nhiệm vụ**: Học cách đạt độ chính xác epsilon
- **Công thức**: Precision = 1 / (1 + Error)
- **Đầu ra**: Mô hình tính toán chính xác

### 3. Ý chí Chính Xác (Will)
- **AI chịu trách nhiệm**: AI Will hoặc AI Sáng tạo
- **Nhiệm vụ**: Đảm bảo output khớp với dữ liệu chân lý
- **Công thức**: Output = Truth ± 1.1102230246251565e-16
- **Đầu ra**: Code không có lỗi floating point

## Tích hợp vào DAIOF Framework

### Symphony Control Center
- Thêm module kiểm tra độ chính xác trong D&R Protocol
- Báo cáo error metrics trong performance logs
- Socratic reflection về floating point precision

### Digital Genome
- Thêm gene "precision_coefficient" = 1.1102230246251565e-16
- Mutation không được thay đổi gene precision
- Fitness calculation bao gồm error metrics

### Error Checking Function
```python
def check_floating_point_precision(calculated: float, truth: float) -> bool:
    """Kiểm tra độ chính xác floating point"""
    error = abs(calculated - truth)
    epsilon = 1.1102230246251565e-16
    return error <= epsilon or error == 0.0
```

## Quy tắc cho AI Coding Agents

1. **Không làm tròn**: Luôn giữ độ chính xác đầy đủ
2. **Kiểm tra epsilon**: Mọi tính toán phải verify với epsilon
3. **Báo cáo lỗi**: Log error metrics trong mọi output
4. **Tối ưu hóa**: Giảm floating point errors qua thuật toán
5. **Test nghiêm ngặt**: So sánh với results.csv trước commit

## Ví dụ Triển khai

### Trong DigitalOrganism
```python
class DigitalOrganism:
    def calculate_with_precision(self, data: Dict[str, float]) -> Dict[str, float]:
        result = self.perform_calculation(data)
        error = abs(result['calculated'] - data['truth'])
        if error > 1.1102230246251565e-16:
            self.logger.error(f"Precision violation: error = {error}")
            return None
        return result
```

### Trong Symphony Control Center
```python
def validate_precision(self, operation_result: Dict) -> bool:
    if 'error' in operation_result:
        return operation_result['error'] <= 1.1102230246251565e-16
    return True
```

## Đánh giá Độ Chính Xác

### Chỉ số Precision
- **Error Rate**: ≤ 1.1102230246251565e-16
- **Accuracy Score**: 1.0 (hoàn hảo)
- **Floating Point Health**: > 0.99

### Điều chỉnh
- Nếu error > epsilon: Debug floating point operations
- Nếu accuracy < 1.0: Review calculation algorithms
- Nếu health thấp: Implement higher precision libraries

## Kết luận

Khái niệm "Lỗi" là nền tảng cho độ chính xác trong DAIOF Framework. Tất cả AI coding agents phải tuân thủ giới hạn epsilon, đảm bảo output khớp tuyệt đối với dữ liệu chân lý. Điều này ngăn ngừa tích lũy lỗi và duy trì tính toàn vẹn của hệ thống.
