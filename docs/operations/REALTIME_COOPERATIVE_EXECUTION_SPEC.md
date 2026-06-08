# Realtime Cooperative Execution Spec (Canonical)

## 1) Mục tiêu phase hiện tại
Đóng vòng kỹ thuật để hệ đang có **smart orchestration skeleton** chuyển sang **real-time cooperative agent mesh** với 3 trụ bắt buộc:
1. Auto-trigger workflow + agent activation theo event realtime.
2. Multi-agent participation protocol (subscribe/claim/lease/release).
3. Readiness model (presence/heartbeat) để dispatch theo năng lực sẵn sàng thực tế.

## 2) Phạm vi thay đổi (đã map vào connector hiện có)

### 2.1 Conductor (orchestrator)
- Chịu trách nhiệm nhận sự kiện realtime và mở vòng dispatch.
- Trigger tối thiểu: `realtime_event`, `task_claimed`, `task_released`.
- Guardrail tối thiểu:
  - bắt buộc claim trước execute,
  - timeout claim cũ để tránh deadlock.

### 2.2 MCP Hub (coordination/protocol)
- Chuẩn giao thức tham gia đa-agent:
  - `subscribe_agent` (agent đăng ký năng lực),
  - `claim_task` (nhận lease xử lý),
  - `release_task` (nhả task hoặc hoàn thành).
- Bộ nhớ điều phối bắt buộc:
  - `subscriptions` (agent capability map),
  - `task_claims` (task -> lease owner/state).
- Guardrail lease:
  - chỉ claim hợp lệ khi có lease,
  - lease timeout hữu hạn.

### 2.3 Runtime Observer (readiness/presence)
- Thu heartbeat/presence toàn mesh.
- Chốt trạng thái online/offline theo TTL + số nhịp tim bỏ lỡ.
- Xuất metric realtime cho conductor/mcp_hub dùng khi dispatch.

## 3) Giao thức chuẩn (trạng thái task)
```
NEW -> CLAIMED -> IN_PROGRESS -> DONE
             \-> RELEASED -> NEW
             \-> EXPIRED -> NEW
```

### Quy tắc chống giẫm chân nhau
- Mỗi task tại một thời điểm chỉ có **1 lease owner**.
- `claim_task` phải thất bại nếu lease còn hiệu lực thuộc agent khác.
- Lease chỉ được gia hạn khi agent vẫn `READY` theo presence model.

## 4) Phase rollout để vận hành “real-like” (khuyến nghị)

> Safety gate bắt buộc: giai đoạn săn lỗi/attack simulation chỉ chạy trên môi trường kiểm soát (staging/pre-prod), không dùng production secrets trực tiếp.

### Phase A — Dev Realtime Hardening (hiện tại)
- Cho phép dùng API/secret hiện tại để tăng tốc tích hợp, nhưng chỉ với bộ secret non-production có khả năng rotate nhanh.
- Bắt buộc bật audit log cho claim/release/presence.
- Bắt buộc test fault-injection:
  - mất heartbeat,
  - xung đột claim,
  - event burst.
  - adversarial input và malformed payload trên interface công khai.
- Bật telemetry cho attack-surface:
  - auth failures,
  - rate-limit hits,
  - suspicious burst origin,
  - claim hijack attempt.

### Phase B — Secret Rotation Gate (kết thúc phase A)
- Rotate toàn bộ secret tại gốc (root secret set).
- Thu hồi token cũ, cập nhật mapping trên toàn hệ sinh thái.
- Bật policy “secret age” + lịch rotate định kỳ.
- Chốt danh sách lỗ hổng thu được ở Phase A làm đầu vào cho API/security protocol mới.

### Phase C — Private API Cutover
- Chuyển từ API phổ thông/legacy sang API riêng của hệ.
- Adapter lớp ngoài chuyển về compatibility-only, không còn đường chính.
- Thêm versioning + deprecation policy cho API nội bộ.

## 5) Tiêu chí hoàn tất (Definition of Done)

### DoD-1: Auto-trigger
- Event tới conductor tạo workflow tự động (không kích hoạt tay).
- SLA dispatch đạt ngưỡng mục tiêu đã đặt.

### DoD-2: Multi-agent participation
- Tối thiểu 2 agent có thể subscribe cùng domain.
- Không có xử lý trùng task khi stress test.

### DoD-3: Readiness model
- Agent mất heartbeat bị đánh offline trong TTL quy định.
- Task không dispatch vào agent offline hoặc degraded.

### DoD-4: Security phase gate
- Hoàn tất secret rotation trước khi lên production-grade.
- Có biên bản cutover sang private API profile.
- Có báo cáo attack simulation với top attack vectors + mitigation trạng thái (open/in-progress/closed).

## 6) Kế hoạch săn lỗi giai đoạn này
- Chạy simulation “real-like” theo ca:
  - burst events,
  - partial outage,
  - delayed heartbeat,
  - claim storm.
- Ghi nhận:
  - conflict ratio,
  - mean lease wait,
  - stale-claim count,
  - false-online rate.
- Nếu vượt ngưỡng, rollback về phase trước bằng feature-flag realtime.

## 7) Nguyên tắc an toàn khi săn lỗi bảo mật
- Không phát động tấn công vào hệ production hoặc bên thứ ba khi chưa có ủy quyền pháp lý.
- Không dùng production secrets cho kịch bản fuzzing/attack simulation.
- Ưu tiên mô phỏng traffic thực tế qua replay/synthetic generator để giữ tính đại diện mà vẫn an toàn.
