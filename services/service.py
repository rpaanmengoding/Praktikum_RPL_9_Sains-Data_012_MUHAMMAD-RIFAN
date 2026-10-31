# Layer Service: Hanya mengurus Logika Bisnis (Aturan Kelulusan)
class PrediksiService:
    def tentukan_kelulusan(self, ipk: float, sks: int) -> str:
        BATAS_IPK_MINIMAL = 3.0
        BATAS_SKS_MINIMAL = 140
        
        if ipk >= BATAS_IPK_MINIMAL and sks >= BATAS_SKS_MINIMAL:
            return "Lulus Tepat Waktu"
        else:
            return "Tidak Lulus"