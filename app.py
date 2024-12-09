import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import nbformat
from nbconvert import HTMLExporter
import io
import contextlib
import sys

# Pengaturan halaman navigasi
st.set_page_config(page_title="Aplikasi Prediksi Konsumsi Listrik", layout="wide")

# Menu navigasi
with st.sidebar:
    selected = option_menu(
        menu_title="Navigasi",
        options=["Halaman Utama", "Analisis MLR", "Unggah Gambar", "Gambar Statis", "Notebook", "Editor Kode"],
        icons=["house", "bar-chart-line", "file-image", "image", "file-earmark-code", "code"],
        default_index=0,
    )

# Halaman Utama
if selected == "Halaman Utama":
    st.title("Selamat Datang di Aplikasi Prediksi Konsumsi Listrik")
    st.write("Diciptakan untuk Solusi Masa Depan yang Lebih Cerdas dan Efisien.")
    st.write("Selamat datang di aplikasi prediksi konsumsi listrik yang dirancang khusus untuk membantu memahami dan memprediksi kebutuhan energi dengan akurat. Aplikasi ini menggabungkan teknologi Multiple Linear Regression (MLR) dengan data yang telah dikumpulkan untuk memberikan prediksi yang akurat dan bermanfaat. Dikembangkan oleh Rifai Machri (NPM: 121055520121124), aplikasi ini tidak hanya membantu dalam analisis konsumsi listrik tetapi juga menjadi alat edukatif bagi Anda yang ingin memahami pola dan efisiensi energi.")
    st.image("16694.jpg")  # Placeholder image

# Halaman Analisis MLR
elif selected == "Analisis MLR":
    st.title("Analisis Multiple Linear Regression (MLR)")
    st.write("Selamat datang di halaman Analisis Multiple Linear Regression (MLR), di mana data berbicara dan keputusan menjadi lebih cerdas! Pada halaman ini, Anda dapat memprediksi konsumsi listrik dengan model statistik yang didukung oleh variabel-variabel penting, seperti Area, Jumlah Penghuni, Jumlah Alat Listrik, dan Jam Penggunaan. Temukan pola, buat prediksi, dan jelajahi berbagai aspek konsumsi energi untuk wawasan yang lebih mendalam!")
    st.write("Konsistensi, keandalan, dan ketepatan dalam setiap prediksi itulah inti dari MLR di aplikasi ini! Masukkan data Anda, lihat hasil analisis, dan temukan peluang untuk mengoptimalkan konsumsi energi di masa depan.")
             
    # Mengunggah data
    uploaded_file = st.file_uploader("Silahkan Unggah file CSV dengan kolom Area, Jumlah_Penghuni, Jumlah_Alat_Listrik, Jam_Penggunaan, dan Konsumsi_Listrik", type="csv")

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        st.write("Data yang diunggah:")
        st.dataframe(data.head())

        # Cek apakah kolom yang diperlukan ada di dalam dataset
        if all(col in data.columns for col in ["Area", "Jumlah_Penghuni", "Jumlah_Alat_Listrik", "Jam_Penggunaan", "Konsumsi_Listrik"]):
            X = data[["Area", "Jumlah_Penghuni", "Jumlah_Alat_Listrik", "Jam_Penggunaan"]]
            Y = data["Konsumsi_Listrik"]
            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=0)

            model = LinearRegression()
            model.fit(X_train, Y_train)
            Y_pred = model.predict(X_test)

            st.write("Koefisien regresi:")
            coef_df = pd.DataFrame(model.coef_, X.columns, columns=["Koefisien"])
            st.write(coef_df)
            st.write("Intercept:", model.intercept_)
            st.write("Mean Squared Error (MSE):", mean_squared_error(Y_test, Y_pred))
            st.write("R-squared:", r2_score(Y_test, Y_pred))

            # Menyimpan nilai intercept dan koefisien untuk digunakan di prediksi otomatis
            intercept = model.intercept_
            b = model.coef_

            # Prediksi Berdasarkan Input Pengguna
            st.subheader("Prediksi Konsumsi Listrik Berdasarkan Input Pengguna")
            Area_input = st.number_input("Masukkan nilai Area (m²)", value=0.0)
            Jumlah_Penghuni_input = st.number_input("Masukkan Jumlah Penghuni", value=0)
            Jumlah_Alat_Listrik_input = st.number_input("Masukkan Jumlah Alat Listrik", value=0)
            Jam_Penggunaan_input = st.number_input("Masukkan Jam Penggunaan", value=0.0)

            # Inisialisasi tabel prediksi jika belum ada
            if "prediction_table" not in st.session_state:
                st.session_state["prediction_table"] = pd.DataFrame(columns=["Area", "Jumlah_Penghuni", "Jumlah_Alat_Listrik", "Jam_Penggunaan", "Prediksi Konsumsi Listrik"])

            if st.button("Prediksi"):
                # Prediksi konsumsi listrik menggunakan rumus regresi linier dengan koefisien dan intercept yang sudah didapat
                prediksi = intercept + b[0] * Area_input + b[1] * Jumlah_Penghuni_input + b[2] * Jumlah_Alat_Listrik_input + b[3] * Jam_Penggunaan_input

                # Masukkan hasil prediksi ke dalam DataFrame
                input_data = pd.DataFrame([[Area_input, Jumlah_Penghuni_input, Jumlah_Alat_Listrik_input, Jam_Penggunaan_input, prediksi]],
                                          columns=["Area", "Jumlah_Penghuni", "Jumlah_Alat_Listrik", "Jam_Penggunaan", "Prediksi Konsumsi Listrik"])

                # Tambahkan hasil prediksi ke tabel di session_state
                st.session_state["prediction_table"] = pd.concat([st.session_state["prediction_table"], input_data], ignore_index=True)
                st.write("Hasil Prediksi:")
                st.dataframe(st.session_state["prediction_table"])

            # Tombol untuk menghapus hasil prediksi
            if st.button("Hapus Hasil Prediksi"):
                st.session_state["prediction_table"] = pd.DataFrame(columns=["Area", "Jumlah_Penghuni", "Jumlah_Alat_Listrik", "Jam_Penggunaan", "Prediksi Konsumsi Listrik"])
                st.write("Hasil prediksi telah dihapus.")

            # Pilihan untuk mengunggah data uji CSV dan memprediksi secara otomatis
            test_file = st.file_uploader("Unggah file CSV untuk Data Test (dengan kolom: Area, Jumlah_Penghuni, Jumlah_Alat_Listrik, Jam_Penggunaan)", type="csv")

            if test_file is not None:
                test_data = pd.read_csv(test_file)
                if all(col in test_data.columns for col in ["Area", "Jumlah_Penghuni", "Jumlah_Alat_Listrik", "Jam_Penggunaan"]):
                    # Melakukan prediksi otomatis berdasarkan data uji
                    test_data["Prediksi Konsumsi Listrik"] = intercept + b[0] * test_data["Area"] + b[1] * test_data["Jumlah_Penghuni"] + b[2] * test_data["Jumlah_Alat_Listrik"] + b[3] * test_data["Jam_Penggunaan"]

                    st.write("Hasil Prediksi Data Uji:")
                    st.dataframe(test_data)

                    # Menyediakan tombol unduhan untuk hasil prediksi
                    csv = test_data.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Unduh Hasil Prediksi sebagai CSV",
                        data=csv,
                        file_name="hasil_prediksi_konsumsi_listrik.csv",
                        mime="text/csv",
                    )
                else:
                    st.error("Data uji harus memiliki kolom: Area, Jumlah_Penghuni, Jumlah_Alat_Listrik, dan Jam_Penggunaan")
        else:
            st.error("Data harus memiliki kolom Area, Jumlah_Penghuni, Jumlah_Alat_Listrik, Jam_Penggunaan, Konsumsi_Listrik")

# Halaman Unggah Gambar
elif selected == "Unggah Gambar":
    st.title("Unggah dan Tampilkan Gambar")
    uploaded_image = st.file_uploader("Unggah gambar", type=["jpg", "png", "jpeg"])
    if uploaded_image is not None:
        st.image(uploaded_image, caption="Gambar yang diunggah", use_column_width=True)

# Halaman Gambar Statis
elif selected == "Gambar Statis":
    st.title("Gambar Statis")
    st.write("Ini adalah gambar statis yang ditampilkan secara otomatis.")
    st.image("16694.jpg", caption="Contoh Gambar Statis", use_column_width=True)

# Halaman Notebook
elif selected == "Notebook":
    st.title("Tampilkan Jupyter Notebook")
    notebook_filename = "MLR.ipynb"
    try:
        with open(notebook_filename, "r", encoding="utf-8") as f:
            notebook_content = nbformat.read(f, as_version=4)

        html_exporter = HTMLExporter()
        html_exporter.template_name = "basic"
        body, resources = html_exporter.from_notebook_node(notebook_content)
        st.components.v1.html(body, height=800, scrolling=True)
    except FileNotFoundError:
        st.error(f"File notebook '{notebook_filename}' tidak ditemukan.")
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat notebook: {e}")

# Halaman Editor Kode
elif selected == "Editor Kode":
    st.title("Editor Kode Python Interaktif")

    # Contoh kode default untuk memandu pengguna
    example_code = """# Contoh kode sederhana
def greet():
    return "Hello AI, pemilik website ini!"

# Menampilkan hasilnya
print(greet())
"""

    # Membuat area input kode dengan contoh kode default
    code_input = st.text_area("Tulis kode Python Anda di sini:", value=example_code, height=200)

    # Tombol untuk menjalankan kode
    if st.button("Jalankan Kode"):
        # Mengarahkan output print() ke dalam StringIO
        output_buffer = io.StringIO()
        
        try:
            # Menjalankan kode dalam konteks output yang diarahkan
            with contextlib.redirect_stdout(output_buffer):
                exec_globals = {}
                exec(code_input, exec_globals)
            
            # Menampilkan hasil output eksekusi kode di website
            output = output_buffer.getvalue()
            if output:  # Cek jika ada output yang dihasilkan
                st.subheader("Hasil Eksekusi Kode:")
                st.code(output)
            else:
                st.subheader("Hasil Eksekusi Kode:")
                st.write("Kode dijalankan tanpa menghasilkan output eksplisit.")
        except Exception as e:
            st.error(f"Terjadi kesalahan saat menjalankan kode: {e}")
        finally:
            output_buffer.close()
