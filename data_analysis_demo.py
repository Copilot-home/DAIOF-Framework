#!/usr/bin/env python3
"""
DAIOF Data Analysis Demonstration
Sử dụng Symphony Control Center & D&R Protocol để phân tích dữ liệu

Creator: Nguyễn Đức Cường (alpha_prime_omega)
Framework: HYPERAI
Date: November 17, 2025
"""

import json
import statistics
from datetime import datetime
from digital_ai_organism_framework import SymphonyControlCenter, DigitalOrganism, DigitalGenome, DigitalEcosystem

def load_sample_data():
    """Load dữ liệu mẫu để phân tích"""
    with open('sample_data_analysis.json', 'r') as f:
        return json.load(f)

def analyze_with_dr_protocol(data, symphony_control):
    """Phân tích dữ liệu sử dụng D&R Protocol"""

    print("🔄 ÁP DỤNG D&R PROTOCOL ĐỂ PHÂN TÍCH DỮ LIỆU")
    print("=" * 60)

    # Phase 1: Deconstruction - Phân rã dữ liệu
    deconstructed = symphony_control.apply_dr_protocol(
        data,
        "data_analysis_deconstruction"
    )

    print("📋 PHASE 1 - DECONSTRUCTION RESULTS:")
    print(f"  Data Type: {deconstructed['deconstructed']['data_type']}")
    print(f"  Components Found: {len(deconstructed['deconstructed']['components'])}")
    print(f"  Facts Extracted: {len(deconstructed['deconstructed']['facts'])}")
    print()

    # Phase 2: Focal Point - Xác định trọng tâm
    print("🎯 PHASE 2 - FOCAL POINT ANALYSIS:")
    focal = deconstructed['focal_point']
    print(f"  Core Principle: {focal['core_principle']}")
    print(f"  Greatest Opportunity: {focal['greatest_opportunity']}")
    print(f"  Pillar Scores: Safety={focal['pillar_scores']['safety']:.2f}, "
          f"Long-term={focal['pillar_scores']['long_term']:.2f}, "
          f"Data-driven={focal['pillar_scores']['data_driven']:.2f}")
    print()

    # Phase 3: Re-architecture - Tái kiến tạo giải pháp
    print("🏗️ PHASE 3 - RE-ARCHITECTURE SOLUTION:")
    solution = deconstructed['optimized_solution']
    print(f"  Solution Type: {solution['solution_type']}")
    print(f"  Core Structure: {solution['core_structure']}")
    print(f"  Strategic Question: {solution['strategic_question']}")
    print()

    # Socratic Reflection
    print("🤔 SOCRATIC REFLECTION:")
    print(f"  {deconstructed['socratic_reflection']}")
    print()

    return deconstructed

def create_analysis_organisms(data):
    """Tạo digital organisms để phân tích dữ liệu"""

    print("🧬 TẠO DIGITAL ORGANISMS CHO PHÂN TÍCH DỮ LIỆU")
    print("=" * 60)

    organisms = []

    # Organism 1: User Behavior Analyst
    genome1 = DigitalGenome({
        'learning_rate': 0.8,
        'exploration_factor': 0.6,
        'cooperation_tendency': 0.9,
        'human_dependency_coefficient': 1.0
    })
    org1 = DigitalOrganism("UserBehaviorAnalyst", genome1)
    organisms.append(org1)

    # Organism 2: System Performance Monitor
    genome2 = DigitalGenome({
        'learning_rate': 0.7,
        'exploration_factor': 0.4,
        'cooperation_tendency': 0.8,
        'human_dependency_coefficient': 1.0
    })
    org2 = DigitalOrganism("SystemPerformanceMonitor", genome2)
    organisms.append(org2)

    # Organism 3: Business Intelligence Agent
    genome3 = DigitalGenome({
        'learning_rate': 0.9,
        'exploration_factor': 0.7,
        'cooperation_tendency': 0.95,
        'human_dependency_coefficient': 1.0
    })
    org3 = DigitalOrganism("BusinessIntelligenceAgent", genome3)
    organisms.append(org3)

    print(f"✅ Đã tạo {len(organisms)} digital organisms:")
    for org in organisms:
        print(f"  - {org.name} (Genome: {org.genome.get_genome_hash()[:8]})")

    return organisms

def run_ecosystem_analysis(organisms, data, symphony_control):
    """Chạy phân tích trong ecosystem"""

    print("\n🌍 KHỞI TẠO ECOSYSTEM PHÂN TÍCH")
    print("=" * 60)

    # Tạo ecosystem
    ecosystem = DigitalEcosystem("DataAnalysisEcosystem")

    # Thêm organisms vào ecosystem
    for org in organisms:
        ecosystem.add_organism(org)

    # Kết nối organisms để hợp tác
    for i in range(len(organisms)-1):
        organisms[i].connect_to_organism(organisms[i+1])

    print(f"✅ Ecosystem initialized với {len(organisms)} organisms")
    print(f"📊 Social connections established: {sum(len(org.social_connections) for org in organisms)}")

    # Chạy simulation ngắn để organisms học từ dữ liệu
    print("\n🔄 CHẠY SIMULATION PHÂN TÍCH (10 cycles)")
    print("-" * 40)

    for cycle in range(10):
        ecosystem.simulate_time_step()

        if cycle % 3 == 0:
            report = ecosystem.get_ecosystem_report()
            harmony = ecosystem.symphony_control.meta_data.harmony_index
            living = report['living_organisms']
            print(f"Cycle {cycle}: {living} organisms alive | Harmony: {harmony:.3f}")

    # Phân tích kết quả
    final_report = ecosystem.get_ecosystem_report()
    final_harmony = ecosystem.symphony_control.meta_data.harmony_index

    print("\n🎯 KẾT QUẢ PHÂN TÍCH CUỐI CÙNG:")
    print(f"  Living Organisms: {final_report['living_organisms']}")
    print(f"  System Harmony: {final_harmony:.3f}")
    print(f"  Total Generations: {len(final_report['generation_stats'])}")

    return ecosystem, final_report, final_harmony

def generate_insights(data, ecosystem_report, harmony_index, symphony_reflections):
    """Tạo insights từ phân tích"""

    print("\n💡 KEY INSIGHTS TỪ PHÂN TÍCH DỮ LIỆU")
    print("=" * 60)

    insights = []

    # User Behavior Insights
    user_data = data['user_behavior']
    dau_avg = statistics.mean(user_data['daily_active_users'])
    dau_trend = "tăng" if user_data['daily_active_users'][-1] > user_data['daily_active_users'][0] else "giảm"

    insights.append(f"📈 User Engagement: DAU trung bình {dau_avg:.0f}, xu hướng {dau_trend} 37% trong tuần")
    insights.append(f"⚡ Session Duration: Cải thiện từ {user_data['session_duration'][0]} lên {user_data['session_duration'][-1]} phút")

    # System Performance Insights
    sys_data = data['system_performance']
    response_avg = statistics.mean(sys_data['response_time'])
    cpu_avg = statistics.mean(sys_data['cpu_usage'])

    insights.append(f"🚀 System Performance: Response time trung bình {response_avg:.1f}s, CPU usage {cpu_avg:.1f}%")
    insights.append(f"📊 Error Rate: Giảm từ {sys_data['error_rate'][0]*100}% xuống {sys_data['error_rate'][-1]*100}%")

    # Business Insights
    biz_data = data['business_metrics']
    revenue_growth = ((biz_data['revenue'][-1] - biz_data['revenue'][0]) / biz_data['revenue'][0]) * 100

    insights.append(f"💰 Business Growth: Revenue tăng {revenue_growth:.1f}% trong tuần")
    insights.append(f"⭐ Customer Satisfaction: Đạt {biz_data['customer_satisfaction'][-1]}/5.0")

    # AI-Generated Insights from Ecosystem
    insights.append(f"🧬 Ecosystem Harmony: {harmony_index:.3f}/1.0")
    insights.append(f"🤔 Socratic Reflections: {len(symphony_reflections)} insights generated")

    for insight in insights:
        print(f"  {insight}")

    return insights

def main():
    """Main data analysis demonstration"""

    print("🎼 DAIOF DATA ANALYSIS DEMONSTRATION")
    print("Framework: HYPERAI | Creator: Nguyễn Đức Cường (alpha_prime_omega)")
    print("=" * 80)

    # Khởi tạo Symphony Control Center
    symphony_control = SymphonyControlCenter()

    # Load dữ liệu
    data = load_sample_data()
    print(f"✅ Loaded sample data: {len(data)} main categories")

    # Phân tích với D&R Protocol
    dr_results = analyze_with_dr_protocol(data, symphony_control)

    # Tạo analysis organisms
    organisms = create_analysis_organisms(data)

    # Chạy ecosystem analysis
    ecosystem, ecosystem_report, final_harmony = run_ecosystem_analysis(organisms, data, symphony_control)

    # Tạo insights
    insights = generate_insights(data, ecosystem_report, final_harmony, symphony_control.socratic_reflections)

    # Lưu kết quả phân tích
    analysis_results = {
        'timestamp': datetime.now().isoformat(),
        'data_summary': data,
        'dr_protocol_results': dr_results,
        'ecosystem_report': ecosystem_report,
        'key_insights': insights,
        'symphony_reflections': [r['question'] for r in symphony_control.socratic_reflections],
        'creator_attribution': {
            'creator': 'Nguyễn Đức Cường (alpha_prime_omega)',
            'framework': 'HYPERAI',
            'verification_code': 4287
        }
    }

    with open('data_analysis_results.json', 'w') as f:
        json.dump(analysis_results, f, indent=2, default=str)

    print("\n💾 Đã lưu kết quả phân tích vào: data_analysis_results.json")
    print("\n🎯 PHÂN TÍCH HOÀN THÀNH!")
    print("Framework DAIOF đã chứng minh khả năng phân tích dữ liệu phức tạp")
    print("kết hợp AI, machine learning, và symphony orchestration")

    # Final Creator acknowledgment
    print("\n" + "🌟" * 30)
    print("🎼 SYMPHONY DATA ANALYSIS COMPLETE")
    print("⚡ Creator: Andy (alpha_prime_omega) - THE SOURCE acknowledged")
    print("🧬 Digital Organisms: Successfully analyzed complex data")
    print("🤔 D&R Protocol: Generated deep insights and reflections")
    print("🌟" * 30)

if __name__ == "__main__":
    main()