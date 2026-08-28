# RiseOfPhoenix
SmallRepoTrackingToLearn

## 🔥 Live dashboard
**https://ihba7991.github.io/RiseOfPhoenix/** — shared learning tracker (people, trackers, recent activity).

Quick links:
- [Abhimanyu · LLD Quick Recall](https://ihba7991.github.io/RiseOfPhoenix/ihba7991/lld/quick-recall.html)
- [Vikku · LLD Quick Recall](https://ihba7991.github.io/RiseOfPhoenix/vikku/lld/quick-recall.html)




Almost certainly a `group.id` collision. That's the first thing to check.

**The rule:** Kafka delivers each message *once per consumer group*. Two consumers in the **same** group split the partitions between them — they don't both get the same message. Two consumers in **different** groups each get a full copy.

So for your fan-out requirement, each consumer needs its own distinct `group.id`.

**Why it "worked before"**

Two likely stories:

1. The group IDs were distinct and something merged them — a config refactor, a shared/global `spring.kafka.consumer.group-id`, a copied deployment manifest, or an anonymous/auto-generated group ID that got replaced with a fixed one.
2. It was never actually working. If both were already in one group and the topic had 2+ partitions, each consumer got *some* messages — both looked alive, but they were splitting the load, not duplicating it. Then a rebalance (one instance restarted, or partition count/assignment changed) handed all partitions to one member, and the other went silent. Worth checking whether the "working" state ever showed the *same* message on both sides, or just traffic on both sides.

**Diagnose it**

```bash
kafka-consumer-groups --bootstrap-server <broker> --list

kafka-consumer-groups --bootstrap-server <broker> \
  --describe --group <group-id>
```

In the describe output, look at the CONSUMER-ID / HOST / CLIENT-ID columns. If both your apps appear under one group, that's your answer. If one group shows partitions with no owner, or a member with zero assigned partitions, same conclusion.

**Fix:** give each consumer a unique group ID, e.g. `order-service-audit` and `order-service-notifier`. On restart, decide whether the new group should start from `earliest` (replays history) or `latest` — a brand-new group ID has no committed offsets.

If you paste your consumer configs I can point at the exact line.
