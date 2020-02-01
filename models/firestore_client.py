from google.cloud import firestore


class FirestoreClient():

    def delete_all(self, collection_name):
        db = firestore.Client()
        collection_ref = db.collection(u'{}'.format(collection_name))
        return self.delete_all_documents(collection_ref=collection_ref,
                                         data=[])

    def delete_all_documents(self, collection_ref=None,
                             batch_size=300,
                             data=None):
        deleted = 0
        docs = collection_ref.limit(batch_size).stream()
        for doc in docs:
            doc.reference.delete()
            data.append(
                {'id': doc.id})
            deleted += 1
        if deleted >= batch_size:
            return self.delete_all_documents(collection_ref=collection_ref,
                                             data=data)
        return data

    def get_all(collection_name, batch_size=300):
        db = firestore.Client()
        documents = db.collection(u'{}'.format(collection_name)).stream()
        for document in documents:
            yield document.id
