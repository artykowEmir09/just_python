questions = [
    "Kendinde en çok sevdiğin 3 özellik ne?",
    "Kendinde değiştirmek istediğin 3 şey ne?",
    "Seni gerçekten mutlu eden şeyler neler?",
    "Hayatta seni en çok korkutan şey ne?",
    "Kimse seni yargılamayacak olsaydı hayatını nasıl yaşardın?",
    "Senin için başarılı olmak ne demek?",
    "10 yıl sonra nasıl bir insan olmak istiyorsun?",
    "Hayatta kesinlikle başarmak istediğin 3 şey ne?",
    "Öldüğünde arkasında nasıl bir hayat bırakmış olmak istersin?",
    "Şu an hiçbir şeyi değiştirmezsen 5 yıl sonra nerede olursun?",
    "Hangi işi yaparken zamanın nasıl geçtiğini fark etmiyorsun?",
    "Para hiç sorun olmasaydı hangi işi yapardın?",
    "Para kazanmak senin için ne kadar önemli?",
    "Kendi şirketini mi kurmak, şirkette yükselmek mi, bağımsız çalışmak mı istersin?",
    "Hayalindeki iş günü nasıl geçiyor?",
    "Dünyada istediğin herhangi bir yerde yaşayabilseydin nerede yaşardın?",
    "Hayatın boyunca mutlaka deneyimlemek istediğin 5 şey ne?",
    "Nasıl bir evde ve çevrede yaşamak istiyorsun?",
    "Sakin bir hayat mı yoksa macera dolu bir hayat mı istiyorsun?",
    "Tamamen özgür olsaydın hayatını nasıl geçirirdin?"
]

answers = []

for i, question in enumerate(questions, start=1):
    print(f"\nSoru {i}: {question}")
    answer = input("Cevabın: ")
    answers.append(answer)

print("\n--- CEVAPLARIN ---")

for i, answer in enumerate(answers, start=1):
    print(f"{i}. {answer}")