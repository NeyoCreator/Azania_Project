use scrypto::prelude::*;

blueprint! {
    struct TokeMachine {
        // Vault to store the remaining dinars
        dinar_vault: Vault,
        // Vault to store the XRD payments
        collected_xrd: Vault,
        // Represents the price to buy a dinars
        price: Decimal
    }

    impl TokeMachine {
        pub fn instantiate_machine(price: Decimal) -> ComponentAddress {
            // Create a new dinar resource
            let dinar_vault: Bucket = ResourceBuilder::new_fungible()
                .divisibility(DIVISIBILITY_NONE)
                .metadata("name", "Dinars")
                .metadata("symbol", "DNH")
                .initial_supply(500);

            // Instantiate a new component and return it
            Self {
                dinar_vault: Vault::with_bucket(dinar_vault),
                collected_xrd: Vault::new(RADIX_TOKEN),
                price: price
            }
            .instantiate().globalize()
        }

        // Allow users to buy a dinar by providing enough XRD.
        // Returns a single dinar and the remaining of the payment bucket (the change)
        pub fn buy_dinar(&mut self, mut payment: Bucket) -> (Bucket, Bucket) {
            info!("Buying a dinar!");
            // Take a portion of the payment bucket depending on the price
            let our_share = payment.take(self.price);

            // Insert the portion of XRD inside the collected_xrd vault
            self.collected_xrd.put(our_share);

            // Take a single dinar
            let dinar: Bucket = self.dinar_vault.take(1);

            // Return the dinar and the XRD remaining in 
            // the payment bucket (if the user sent too much)
            (dinar, payment)
        }
    }
}
